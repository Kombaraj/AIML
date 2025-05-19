
Section 1: Course Introduction
    Slides: AWS-Bedrock-Multi-Agents-Course_v1.0.pdf

Section 2: Evolution of AI Agents & Core Capabilities


Section 3: Deep Dive - Amazon Bedrock Agents
    Amazon Bedrock Agent is a fully managed service that enable generative AI applications to automate multistep tasks by seamlessly connecting with Internal corporate systems, APIs and data sources.



Section 4: Use Case 1 - Hotel Room Booking Agent
    Agent Creation => Bedrock -> Builder Tools -> Agents -> Create Agent
        Name: "Hotel_Room_Booking_Agent"
        Agent Resource Role - Create new (or existing)
        Select Model - Amazon Nova Pro [Or Anthropic Claude 3 Sonnet Or Titan Text G1 Premier - which doesn't support long-term memory support]
        Instructions to the Agent - Take it from "Agent_Instructions.pdf"
            "You are a Hotel Booking Agent can do following :
                • Answer queries related to hotel rooms
                • Query and display room availability for a particular date
                • Book a hotel room based on user provided details such as check in date, room type, guest name, number of nights and share back the booking id."
        Additional Settings -> User Input - Enabled
        Memory - Enabled
        Save & Exit
        Prepare
        Simple test with "Hi" message
    Hotel Rooms Details 
        Agent Integration with Knowledge Bases for Room Information
            Create S3 bucket - "s3roominformation2025"
            Upload the PDF "Use Case 1\Use Case 1- Code - 15032025\Taj-Fort-Aguada-Resort&Spa-Goa.pdf"
        Create Knowledge Base 
            Bedrock -> Builder Tools -> Knowledge Bases -> Create KB with vector store - "RoomInformation-KB"
            IAM Permissions -> Create and use a new service role
            Configure data source -> Amazon S3 -> 
                Data source name - "knowledge-base-quick-start-ul39v-data-source"
                S3 URI - "s3://s3roominformation2025"
                Parsing Strategy - Default
                Chunking Strategy - Default
            Configure data storage and processing
                Embedding Model - "Titan Text Embedding v2"
            Vector Database -> Quick create a new vector store (Recommended) -> Amazon OpenSearch Serverless
            Create Knowkedge Base Button
            Data source -> Sync
            Test KB -> Select Model -> Amazon Nova Pro  -> "What are the sea view rooms available?"
            Copy KB ID
        Configure Agent with KB
            Goto Agent -> KB -> Add -> Select "RoomInformation-KB"
                            -> KB Instructions for Agent
                            "As an agent route any question by the user related to room type, room amenities, room description, hotel location to the knowledge bases"
            Save & Exit -> Prepare -> Test - "What are the dining options at Taj?"
    Hotel Rooms Availability
        Architecture and DynamoDB Creation
            DynamoDB Table - "hotelRoomAvailabilityTable"
                Partition Key - "date" - string
                Create Item -> date = "2025-12-25"
                               seaView = "0"
                               gardenView = "0"
                Add few more items
        Action Group 1 - Lambda Function & OpenAPI Schema Creation
            Lambda Function - "hotelRoomAvailabilityFunction"
                Set time out - 1 min
                Permission - AdministratorAccess
                Local Testing -> Test -> Configure Test Event-> Event Name "Test"
                                                            Event JSON: {
                                                                "checkInDate": "2025-12-25"
                                                            }
                                                            Save
                Code - "hotelRoomAvailabilityFunction.zip"
            OpenAPI Schema and Integration with Agent
                Goto Agent -> Edit in Agent Builder -> Action Groups -> Add - "action_group_roomAvailability"
                    Action Group type - Define with API schemas
                    Action group invocation - Select an existing Lambda Function "hotelRoomAvailabilityFunction"
                    Action group schema - Define via in-line schema editor -> copy & paste content from "Hotel Room Availability_OpenAPISchema.yaml"
                Save & Exit
                Prepare
            Allow the Agent to access the Lambda Function
                Goto Lambda function "hotelRoomAvailabilityFunction"
                    Configuration -> Resource-based policy statements -> Add Permissions -> AWS Service -> Others (As of now no Service available for Agents) 
                        Statement ID - "hotel-booking-inventory"
                        Principal - "bedrock.amazonaws.com"
                        Source ARN - Bedrock Agent's ARN
                        Action - "lambda:InvokeFunction"
            Test the Agent for Room availability
    Hotel Rooms Booking
        DynamoDB Creation 
            Name - "hotelRoomBookingTable"
            Partition Key - "bookingID" - String
            Items: checkInDate, roomType, guestName, numberofNights
        Action Group 2 - Lambda Function & OpenAPI Schema Creation
            Lambda Function - "hotelRoomBookingFunction"
                Set time out - 1 min
                Permission - AdministratorAccess
                Local Testing -> Test -> Configure Test Event-> Event Name "Test"
                                                            Event JSON: {
                                                                "checkInDate": "2025-12-25",
                                                                "roomType": "Beach gardenView",
                                                                "guestName": "Raj",
                                                                "numberofNights": "2"
                                                            }
                                                            Save
                Code - "hotelRoomBookingFunction.zip"
            OpenAPI Schema and Integration with Agent
                Goto Agent -> Edit in Agent Builder -> Action Groups -> Add - "action_group_hotlRoomBooking"
                    Action Group type - Define with API schemas
                    Action group invocation - Select an existing Lambda Function "hotelRoomBookingFunction"
                    Action group schema - Define via in-line schema editor -> copy & paste content from "Hotel Room Booking_OpenAPISchema.yaml"
                Save & Exit
                Prepare
            Allow the Agent to access the Lambda Function
                Goto Lambda function "hotelRoomBookingFunction"
                    Configuration -> Resource-based policy statements -> Add Permissions -> AWS Service -> Others (As of now no Service available for Agents) 
                        Statement ID - "roombooking-agent-01"
                        Principal - "bedrock.amazonaws.com"
                        Source ARN - Bedrock Agent's ARN
                        Action - "lambda:InvokeFunction"
            Test the Agent for Room Booking
    Agent Guardrails and Memory setup
        Bedrock -> Safeguards -> Guardrails -> Create Guardrails 
            Name - "HotelBookingGuardrails"
            Harmful categories
            Add denied topic
            Add word filter
            Add sensitive information filters
            Add contextual grounding check
            Review & Create
            Select Model - Amazon Nova Pro
                Prompt - "Who is the guest staying corresponding to bookingID - 12Be155"
            
        Configure Agent to use Guardrails
            Goto Agent -> Guardrails details -> Select the Guardrail "HotelBookingGuardrails"
            Save & Exit -> Prepare
        Memory setup
            Goto Agent -> Memory -> Enabled
                Momory duration - 30 days
            Save & Exit -> Prepare
    Agent Version and Alias deployment
        Goto Agent -> Alaias -> Create
            Alias name - "dev"
            Associate a version - "Create a new version and associate it to this alias"
            Alias and Version are created
    Streamlit UI Pre-requisites
    Agent UI deployment with Streamlit
        Code Path: Use Case 1/Use Case 1- Code - 15032025/UI_Local/amazon-bedrock-agent-test-ui-main
        streamlit run app.py
    Final demo
    Fronend Deployment to EC2 Server
    Add Application Load Balancer to EC2

Section 5: Use Case 2 - Enterprise Travel Agent (Multi-Agent)
    Use Case Architecture

    Collaborator Agent 1 - HR Agent
        Backend and Agent Creation
            DynamoDB - "leaveBalanceHRTable"
                Partition Key - "empID" - Number
                Create Items (Few Records)
                    empID - Number
                    employeeName - String
                    leaveBalance - Number
            HR Agent 
                Bedrock -> Builder Tools -> Agent -> "HR_Agent"
                    Model - Amazon Nova Pro
                    Agent Instructions - Copy from PDF
                    User Input - Enabled
                    Save & Exit -> Prepare
        Lambda Creation & Agent Integration
            Lambda - "leaveBalanceHRFunction" (leaveBalanceHRFunction_Lambda.zip)
                Set time out - 1 min
                Permission - AmazonDynamoDBFullAccess
            OpenAPI Schema and Integration with Agent
                Agent -> Action Group -> "retrieveLeaveBalance"
                Action Group invocation -> Select an existing Lambda Function - "leaveBalanceHRFunction"
                Action Group Schema -> Define via in-line schema editor -> "retrieveLeaveBalance_OpenAPISchema.yaml"
                Save & Exit -> Prepare
            Allow the Agent to access the Lambda Function
                Goto Lambda function "leaveBalanceHRFunction"
                    Configuration -> Resource-based policy statements -> Add Permissions -> AWS Service -> Others (As of now no Service available for Agents) 
                        Statement ID - "hr-agent-01"
                        Principal - "bedrock.amazonaws.com"
                        Source ARN - Bedrock Agent's ARN
                        Action - "lambda:InvokeFunction"
            Test the Agent
        Bedrock Knowledge Base
            Create S3 bucket - "hrpolicyagent01" and upload "Knowledge Base _ HR Policy Document.pdf"
            Create Knowledge Base 
                Bedrock -> Builder Tools -> Knowledge Bases -> Create KB with vector store - "hrPolicyAgent01"
                IAM Permission -> Create new role
                Choose data source -> S3 -> "hrpolicyagent01"
                Parsing Strategy - Default
                Chunking Strategy - Default
                Embedding Model - "Titan Text Embedding v2"
                Vector Database -> Quick Create a new vector store -> Amazon OpenSearch Serverless
                Create Knowkedge Base Button
                Data source -> Sync
                Test KB -> Select Model -> Nova Pro -> "Number of annual leave for full time employee?"
                Copy KB ID
        Configure Agent with KB
            Goto Agent "HR_Agent" -> KB -> Add -> Select "hrPolicyAgent01"
                            -> KB Instructions for Agent
                            "Answer any user question related to HR Leave Policy such as Annual Leave, Sick leave and number of days entitled for each leave type."
            Save & Exit -> Prepare -> Test - "Number of annual leave for part time employee?"
                                   -> Test - "Leave balance for the employee id 42675?"               
        Agent Version and Alias deployment
            Goto Agent "HR_Agent" -> Alaias -> Create
                Alias name - "dev"
                Associate a version - "Create a new version and associate it to this alias"
                Alias and Version are created   

    Collaborator Agent 2 - Hotel Room Booking Agent     
        Covered this agent in Use Case 1

    Supervisor Agent - Enterprise Travel Agent
        Agent - "Enterprise_Travel_Agent"
        Enable Multi-Agent collaboration - ON
        Select Model - Amazon Nova Pro
        Instructions for the Supervisor Agent:
            "You are an enterprise travel agent. You are supervisor agent and have 2 collaborator agents – HR Agents and Hotel Booking Agents. The HR Agent can be used to answer questions about your leave policy and get leave balance. The Hotel Booking Agent can be used to checking the hotel room details, check the room availability for a particular date and book a hotel room based on user provided details such as check in date, room type, guest name and number of nights."
        User Input - Enabled
        Multi-agent collaboration
            Edit -> Collaboration status - Make sure it's enabled
                    Collaboration Configuration - Select "Supervisor" option
                    Add Collaborator 1 -> 
                        Collaborator Name - "HRAgent"
                        Collaborator Agent - "HR_Agent" & Agent Alias "dev"
                        Collaborator Instructions:
                            "You are an HR Agent can be used for following
                                - Answer questions about your leave policy
                                - Query and display leave balances for employee based on employee id
                                - Answer frequently asked questions (FAQs) about HR policies"
                        Enable conversation history sharing - ON
                    Add Collaborator 2 -> 
                        Collaborator Name - "HotelRoomBookingAgent"
                        Collaborator Agent - "Hotel_Room_Booking_Agent" & Agent Alias "dev"
                        Collaborator Instructions:
                            "You are a Hotel Booking Agent can do following :
                            • Answer queries related to hotel rooms
                            • Query and display room availability for a particular date
                            • Book a hotel room based on user provided details such as check in date, room type, guest name, number of nights and share back the booking id."
                        Enable conversation history sharing - ON
            Agent Permission
                Edit in Agent Builder
                    Role - Assign "AmazonBedrockFullAccess"
            Save & Exit -> Prepare
            Test
                "What's the leave balance of empID 200343?"
                "Room availability for 2025-12-25"
            Agent Version and Alias deployment
                Goto Agent -> Alaias -> Create
                    Alias name - "dev"
                    Associate a version - "Create a new version and associate it to this alias"
                    Alias and Version are created                
            Agent UI deployment with Streamlit
                Code Path: Use Case 2\Use Case 2_22Feb2025\UI\amazon-bedrock-agent-test-ui-main
                streamlit run app.py
            Final demo
                "What's the leave balance of empID 200343?"
                "Book a hotel for employee ID 200343 if the leave balance is more than 3 days with below details, date of booking 2025-12-27, Name - John, number of days 2 and room type Sea view"