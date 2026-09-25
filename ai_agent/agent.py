# from .tools import (
#     get_maintenance_history,
#     find_available_technicians,
#     check_appointment_slot,
#     book_appointment,
# )


# class SmartCarAgent:
#     """
#     Core Agent for the Smart Car Service System.

#     Flow:
#     Goal Perception
#         ↓
#     Reasoning / Tool Selection
#         ↓
#     Action Execution
#         ↓
#     Observation / Feedback
#         ↓
#     Task Completion
#     """

#     def __init__(self, user):
#         self.user = user

#     def perceive_goal(self, user_input):
#         """
#         Understand the user's request and identify the goal.
#         """

#         text = user_input.lower().strip()

#         if "maintenance" in text or "صيانة" in text:
#             goal = "maintenance_history"

#         elif "technician" in text or "فني" in text:
#             goal = "available_technicians"

#         elif "appointment" in text or "حجز" in text or "موعد" in text:
#             goal = "appointment"

#         else:
#             goal = "unknown"

#         return {
#             "user_input": user_input,
#             "goal": goal,
#         }

#     def select_tool(self, goal):
#         """
#         Select the appropriate tool according to the detected goal.
#         """

#         tools = {
#             "maintenance_history": get_maintenance_history,
#             "available_technicians": find_available_technicians,
#             "appointment": book_appointment,
#         }

#         return tools.get(goal)

#     def execute_tool(self, tool, **kwargs):
#         """
#         Execute the selected tool.
#         """

#         if tool is None:
#             return {
#                 "success": False,
#                 "message": "I could not determine the required action.",
#             }

#         return tool(
#             user=self.user,
#             **kwargs,
#         )

#     def observe(self, result):
#         """
#         Observe the result returned by the tool.
#         """

#         return result

#     def complete(self, observation):
#         """
#         Produce the final agent result.
#         """

#         return observation

#     # def run(self, user_input, **kwargs):
#     #     """
#     #     Execute the complete Agentic AI flow.
#     #     """

#     #     perception = self.perceive_goal(user_input)

#     #     goal = perception["goal"]
#     #     tool = self.select_tool(goal)

#     #     result = self.execute_tool(
#     #         tool,
#     #         **kwargs,
#     #     )

#     #     observation = self.observe(result)

#     #     return self.complete(observation)
    
#     def run(self, user_input, **kwargs):
#         """
#         Execute the complete Agentic AI flow.
#         """

#         perception = self.perceive_goal(user_input)

#         goal = perception["goal"]
#         tool = self.select_tool(goal)

#         parameters = self.extract_parameters(
#             goal=goal,
#             user_input=user_input,
#             **kwargs,
#         )

#         result = self.execute_tool(
#             tool,
#             **parameters,
#         )

#         observation = self.observe(result)

#         return self.complete(observation)
    
#     def extract_parameters(self, goal, user_input, **kwargs):
#         """
#         Extract and validate the parameters required by the selected tool.

#         For now, parameters are supplied explicitly to the Agent.
#         Later, the LLM will extract them from natural language.
#         """

#         if goal == "maintenance_history":
#             if "car_id" not in kwargs:
#                 raise ValueError("car_id is required.")

#             return {
#                 "car_id": kwargs["car_id"],
#             }

#         if goal == "available_technicians":
#             return {}

#         if goal == "appointment":
#             required_parameters = [
#                 "car_id",
#                 "technician_id",
#                 "service_type",
#                 "appointment_date",
#                 "appointment_time",
#             ]

#             missing_parameters = [
#                 parameter
#                 for parameter in required_parameters
#                 if parameter not in kwargs
#             ]

#             if missing_parameters:
#                 raise ValueError(
#                     f"Missing required parameters: {', '.join(missing_parameters)}"
#                 )

#             return {
#                 "car_id": kwargs["car_id"],
#                 "technician_id": kwargs["technician_id"],
#                 "service_type": kwargs["service_type"],
#                 "appointment_date": kwargs["appointment_date"],
#                 "appointment_time": kwargs["appointment_time"],
#                 "notes": kwargs.get("notes", ""),
#             }

#         return {}

# import json
# from django.core.exceptions import ValidationError
# from google import genai
# from google.genai import types,errors
# from django.conf import settings
# from datetime import date, time, datetime
# from .tools import (
#     get_maintenance_history,
#     find_available_technicians,
#     check_appointment_slot,
#     book_appointment,
#     find_low_stock_spare_parts,
#     get_my_appointments_for_ai,)
# from cars.models import Car
# from .tools import get_my_cars_for_ai


# class SmartCarAgent:
#     """
#     Smart Car Agent.

#     Flow:
#     User Input
#         ↓
#     LLM Reasoning
#         ↓
#     Tool Selection
#         ↓
#     Parameter Validation
#         ↓
#     Tool Execution
#         ↓
#     Observation
#         ↓
#     Final Response
#     """

#     def __init__(self, user):
#         self.user = user

#         self.client = genai.Client(
#             api_key=settings.GEMINI_API_KEY
#         )
        
#         self.pending_action = None

#         self.tools = {
#             "get_maintenance_history": get_maintenance_history,
#             "find_available_technicians": find_available_technicians,
#             "check_appointment_slot": check_appointment_slot,
#             "book_appointment": book_appointment,
#             "find_low_stock_spare_parts": find_low_stock_spare_parts,
#             "get_my_cars": get_my_cars_for_ai,
#             "get_my_appointments": get_my_appointments_for_ai,}
        
#         self.function_declarations = [
            
#             types.FunctionDeclaration(
#     name="get_my_cars",
#     description="Get the cars owned by the currently authenticated user.",
#     parameters=types.Schema(
#         type="OBJECT",
#         properties={},
#     ),
# ),          types.FunctionDeclaration(
#     name="get_my_appointments",
#     description="Get all appointments belonging to the currently authenticated user.",
#     parameters=types.Schema(
#         type="OBJECT",
#         properties={},
#     ),
# ),
#             types.FunctionDeclaration(
#         name="get_maintenance_history",
#         description="Get the maintenance history of a specific car.",
#         parameters=types.Schema(
#             type="OBJECT",
#             properties={
#                 "car_id": types.Schema(
#                     type="INTEGER",
#                     description="The ID of the car."
#                 )
#             },
#             required=["car_id"],
#         ),
#     ),

#             types.FunctionDeclaration(
#         name="find_available_technicians",
#         description="Find technicians who are currently available.",
#         parameters=types.Schema(
#             type="OBJECT",
#             properties={},
#         ),
#     ),

#             types.FunctionDeclaration(
#     name="check_appointment_slot",
#     description="Check whether a technician appointment slot is available.",
#     parameters=types.Schema(
#         type="OBJECT",
#         properties={
#             "technician_id": types.Schema(
#                 type="INTEGER",
#                 description="The technician ID."
#             ),
#             "appointment_date": types.Schema(
#                 type="STRING",
#                 description="Appointment date in YYYY-MM-DD format."
#             ),
#             "appointment_time": types.Schema(
#                 type="STRING",
#                 description="Appointment time in HH:MM format."
#             ),
#         },
#         required=[
#             "technician_id",
#             "appointment_date",
#             "appointment_time",
#         ],
#     ),
# ),

#             types.FunctionDeclaration(
#         name="book_appointment",
#         description="Book a service appointment for a user's car.",
#         parameters=types.Schema(
#             type="OBJECT",
#             properties={
#                 "car_id": types.Schema(
#                     type="INTEGER",
#                     description="The user's car ID."
#                 ),
#                 "technician_id": types.Schema(
#                     type="INTEGER",
#                     description="The technician ID."
#                 ),
#                 "service_type": types.Schema(
#                     type="STRING",
#                     description="Type of service requested."
#                 ),
#                 "appointment_date": types.Schema(
#                     type="STRING",
#                     description="Appointment date in YYYY-MM-DD format."
#                 ),
#                 "appointment_time": types.Schema(
#                     type="STRING",
#                     description="Appointment time in HH:MM format."
#                 ),
#                 "notes": types.Schema(
#                     type="STRING",
#                     description="Optional appointment notes."
#                 ),
#             },
#             required=[
#                 "car_id",
#                 "technician_id",
#                 "service_type",
#                 "appointment_date",
#                 "appointment_time",
#             ],
#         ),
#     ),
#             types.FunctionDeclaration(
#     name="find_low_stock_spare_parts",
#     description="Find spare parts whose stock quantity is at or below the minimum stock level.",
#     parameters=types.Schema(
#         type="OBJECT",
#         properties={},
#     ),
# ),
# ]

#     def perceive_goal(self, user_input):
#         """
#         Ask the LLM to understand the user's goal.
#         """

#         prompt = f"""
# You are the reasoning component of a Smart Car Service system.

# Analyze the user's request and return ONLY valid JSON.

# Available goals:

# 1. maintenance_history
# 2. available_technicians
# 3. appointment
# 4. unknown

# User request:
# {user_input}

# Return exactly:

# {{
#     "goal": "one of the available goals",
#     "reason": "short explanation"
# }}
# """

#         response = self.client.models.generate_content(
#             model="gemini-3.5-flash-lite",
#             contents=prompt,
#         )

#         try:
#             return json.loads(response.text)
#         except json.JSONDecodeError:
#             return {
#                 "goal": "unknown",
#                 "reason": "The model returned invalid JSON.",
#             }

#     def select_tool(self, goal):
#         """
#         Map the goal to an approved backend tool.
#         """

#         goal_to_tool = {
#             "maintenance_history": "get_maintenance_history",
#             "available_technicians": "find_available_technicians",
#             "appointment": "book_appointment",
#         }

#         tool_name = goal_to_tool.get(goal)

#         if not tool_name:
#             return None

#         return self.tools.get(tool_name)

#     def extract_parameters(self, goal, user_input):
#         """
#         Extract parameters from the user's request.

#         This stage currently returns only the parameters
#         that can safely be inferred from the conversation.
#         """

#         prompt = f"""
# You are extracting parameters for a Smart Car Service system.

# User request:
# {user_input}

# Detected goal:
# {goal}

# Return ONLY valid JSON.

# For maintenance_history:
# {{
#     "car_id": null
# }}

# For available_technicians:
# {{}}

# For appointment:
# {{
#     "car_id": null,
#     "technician_id": null,
#     "service_type": null,
#     "appointment_date": null,
#     "appointment_time": null,
#     "notes": ""
# }}
# """

#         response = self.client.models.generate_content(
#             model="gemini-3.5-flash-lite",
#             contents=prompt,
#         )

#         try:
#             return json.loads(response.text)
#         except json.JSONDecodeError:
#             raise ValidationError(
#                 "The AI returned invalid parameters."
#             )

#     def execute_tool(self, tool, parameters):
#         """
#         Execute only an approved backend tool.
#         """

#         if tool is None:
#             return {
#                 "success": False,
#                 "message": "No suitable tool was found.",
#             }

#         return tool(
#             user=self.user,
#             **parameters,
#         )

#     def observe(self, result):
#         """
#         Observe the tool result.
#         """

#         return result

#     def complete(self, observation):
#         """
#         Return the final result.
#         """

#         return observation

#     def run(self, user_input):
#         """
#         Execute the complete Agentic AI pipeline.
#         """

#         perception = self.perceive_goal(user_input)

#         goal = perception.get("goal", "unknown")

#         if goal == "unknown":
#             return {
#                 "success": False,
#                 "message": "I could not determine what you want to do.",
#             }

#         tool = self.select_tool(goal)

#         if tool is None:
#             return {
#                 "success": False,
#                 "message": "No suitable tool is available.",
#             }

#         parameters = self.extract_parameters(
#             goal,
#             user_input,
#         )

#         result = self.execute_tool(
#             tool,
#             parameters,
#         )

#         observation = self.observe(result)

#         return self.complete(observation)
    
#     def choose_function(self, user_input):
#         """
#         Ask Gemini to choose one approved backend function.
#         Gemini does not execute the function.
#         """

#         response = self.client.models.generate_content(
#             model="gemini-3.5-flash-lite",
#             contents=user_input,
#             config=types.GenerateContentConfig(
#             tools=[
#                 types.Tool(
#                     function_declarations=self.function_declarations
#                 )
#             ],
#             automatic_function_calling=types.AutomaticFunctionCallingConfig(
#                 disable=True
#             ),
#         ),
#     )

#         if not response.function_calls:
#             return {
#             "function_name": None,
#             "arguments": {},
#             "text": response.text,
#         }

#         function_call = response.function_calls[0]

#         return {
#         "function_name": function_call.name,
#         "arguments": dict(function_call.args),
#     }
        
#     def execute_function_call(self, function_name, arguments):
#         """
#         Execute only functions that are explicitly registered
#         in the Agent's tool whitelist.
#         """

#         if not function_name:
#             return {
#             "success": False,
#             "message": "No function was requested.",
#         }

#         tool = self.tools.get(function_name)

#         if tool is None:
#             return {
#             "success": False,
#             "message": "Requested function is not allowed.",
#         }

#         try:
#             result = tool(
#             user=self.user,
#             **arguments,
#         )

#             return {
#             "success": True,
#             "function_name": function_name,
#             "result": result,
#         }

#         except ValidationError as exc:
#             return {
#             "success": False,
#             "function_name": function_name,
#             "message": str(exc),
#         }    
            
#     # def run_agent_loop(self, user_input):
#     #     """
#     #     Full Agentic AI loop.

#     #     Gemini decides whether a backend tool is needed.
#     #     The Agent executes only approved tools.
#     #     The tool result is then returned to Gemini
#     #     to generate the final natural-language response.
#     #     """

#     #     response = self.client.models.generate_content(
#     #         model="gemini-3.5-flash-lite",
#     #         contents=user_input,
#     #         config=types.GenerateContentConfig(
#     #         tools=[
#     #             types.Tool(
#     #                 function_declarations=self.function_declarations
#     #             )
#     #         ],
#     #         automatic_function_calling=types.AutomaticFunctionCallingConfig(
#     #             disable=True
#     #         ),
#     #     ),
#     # )

#     #     if not response.function_calls:
#     #         return {
#     #         "success": True,
#     #         "tool_used": False,
#     #         "answer": response.text,
#     #     }

#     #     function_call = response.function_calls[0]

#     #     function_name = function_call.name
#     #     arguments = dict(function_call.args)

#     #     execution = self.execute_function_call(
#     #     function_name,
#     #     arguments,
#     # )

#     #     return {
#     #     "success": execution["success"],
#     #     "tool_used": True,
#     #     "function_name": function_name,
#     #     "arguments": arguments,
#     #     "tool_result": execution,
#     # }        
    
# #     def run_agent_loop(self, user_input):
# #         """
# #         Full Agentic AI loop.

# #         Flow:
# #         User Input
# #         -> Gemini Tool Selection
# #         -> Approved Tool Execution
# #         -> Tool Result
# #         -> Gemini Final Answer
# #         """

# #         response = self.client.models.generate_content(
# #             model="gemini-3.5-flash-lite",
# #             contents=user_input,
# #             config=types.GenerateContentConfig(
# #                 tools=[
# #                     types.Tool(
# #                         function_declarations=self.function_declarations
# #                     )
# #                 ],
# #                 automatic_function_calling=types.AutomaticFunctionCallingConfig(
# #                     disable=True
# #                 ),
# #             ),
# #         )

      
# #         if not response.function_calls:
# #             return {
# #                 "success": True,
# #                 "tool_used": False,
# #                 "answer": response.text,
# #             }


# #         function_call = response.function_calls[0]

# #         function_name = function_call.name
# #         arguments = dict(function_call.args)

        
# #         if self.requires_confirmation(function_name):
# #             return self.build_confirmation_request(
# #                 function_name,
# #                 arguments,)
            
# #         execution = self.execute_function_call(
# #             function_name,
# #             arguments,)

# #         if not execution["success"]:
# #             return {
# #                 "success": False,
# #                 "tool_used": True,
# #                 "function_name": function_name,
# #                 "arguments": arguments,
# #                 "error": execution.get(
# #                     "message",
# #                     "Tool execution failed."
# #                 ),
# #             }


# #         tool_result = execution["result"]

# #         # if function_name == "check_appointment_slot":
# #         #     if tool_result.get("available") is True:
# #         #         return {
# #         #             "success": True,
# #         #             "tool_used": True,
# #         #             "function_name": function_name,
# #         #             "arguments": arguments,
# #         #             "tool_result": tool_result,
# #         #             "confirmation_required": True,
# #         #             "next_action": "book_appointment",
# #         #             "message": (
# #         #                 "The appointment slot is available.\n\n"
# #         #                 "Please confirm the following appointment:\n"
# #         #                 f"- Technician: {tool_result['technician']['name']}\n"
# #         #                 f"- Specialization: {tool_result['technician']['specialization']}\n"
# #         #                 f"- Date: {tool_result['appointment_date']}\n"
# #         #                 f"- Time: {tool_result['appointment_time']}\n\n"
# #         #                 "Do you confirm this appointment?"
# #         #             ),
# #         #         }
# #         if function_name == "check_appointment_slot":
# #             if tool_result.get("available") is True:

# #                 self.pending_action = {
# #                     "function_name": "book_appointment",
# #                     "arguments": {
# #                         "car_id": arguments.get("car_id"),
# #                         "technician_id": arguments.get("technician_id"),
# #                         "service_type": arguments.get("service_type"),
# #                         "appointment_date": arguments.get("appointment_date"),
# #                         "appointment_time": arguments.get("appointment_time"),
# #                         "notes": arguments.get("notes", ""),
# #                     },
# #                 }

# #                 return {
# #                     "success": True,
# #                     "tool_used": True,
# #                     "function_name": function_name,
# #                     "arguments": arguments,
# #                     "tool_result": tool_result,
# #                     "confirmation_required": True,
# #                     "next_action": "book_appointment",
# #                     "message": (
# #                         "The appointment slot is available.\n\n"
# #                         "Please confirm the following appointment:\n"
# #                         f"- Car ID: {arguments.get('car_id')}\n"
# #                         f"- Technician: {tool_result['technician']['name']}\n"
# #                         f"- Specialization: {tool_result['technician']['specialization']}\n"
# #                         f"- Service: {arguments.get('service_type')}\n"
# #                         f"- Date: {tool_result['appointment_date']}\n"
# #                         f"- Time: {tool_result['appointment_time']}\n\n"
# #                         "Do you confirm this appointment?"
# #                     )
# #                 }
                
# #         final_prompt = f"""
# # You are the final response generator for a Smart Car Service System.

# # The user asked:
# # {user_input}

# # The backend tool that was executed:
# # {function_name}

# # The tool result is:
# # {tool_result}

# # Using only the tool result, provide a clear and concise
# # answer to the user.

# # Do not invent information.
# # Do not mention internal tools, function calling,
# # database, ORM, or implementation details.
# # """

# #         final_response = self.client.models.generate_content(
# #             model="gemini-3.5-flash-lite",
# #             contents=final_prompt,
# #         )


# #         return {
# #             "success": True,
# #             "tool_used": True,
# #             "function_name": function_name,
# #             "arguments": arguments,
# #             "tool_result": tool_result,
# #             "answer": final_response.text,
# #         }

#     def run_agent_loop(self, user_input):


#         if self.pending_action:

#             confirmation = user_input.strip().lower()

#             if confirmation in [
#             "yes",
#             "y",
#             "confirm",
#             "confirmed",
#             "approve",
#             "ok",
#             "okay",
#         ]:

#                 result = self.confirm_pending_action(True)

#                 if result["success"]:

#                     appointment = result["result"]["appointment"]

#                     return {
#                     "success": True,
#                     "tool_used": True,
#                     "function_name": "book_appointment",
#                     "confirmation_required": False,
#                     "answer": (
#                         "Appointment booked successfully.\n\n"
#                         f"Car: {appointment['car']}\n"
#                         f"Technician: {appointment['technician']}\n"
#                         f"Service: {appointment['service_type']}\n"
#                         f"Date: {appointment['appointment_date']}\n"
#                         f"Time: {appointment['appointment_time']}\n"
#                         f"Status: {appointment['status']}"
#                     ),
#                 }

#                 return {
#                 "success": False,
#                 "tool_used": True,
#                 "function_name": "book_appointment",
#                 "confirmation_required": False,
#                 "error": result.get(
#                     "message",
#                     "The appointment could not be booked.",
#                 ),
#             }


#             if confirmation in [
#             "no",
#             "n",
#             "cancel",
#             "cancelled",
#             "decline",
#             "reject",
#         ]:

#                     result = self.confirm_pending_action(False)

#                     return {
#                 "success": True,
#                 "tool_used": False,
#                 "confirmation_required": False,
#                 "answer": result["message"],
#             }


#             return {
#             "success": True,
#             "tool_used": False,
#             "confirmation_required": True,
#             "pending_action": self.pending_action,
#             "message": (
#                 "I have a pending appointment booking.\n\n"
#                 "Please reply with Yes to confirm or No to cancel."
#             ),
#         }


    

#         booking_keywords = [
#         "book",
#         "booking",
#         "appointment",
#         "schedule",
#         "reserve",
#     ]

#         is_booking_request = any(
#         keyword in user_input.lower()
#         for keyword in booking_keywords
#     )


    

#         if is_booking_request:

#             booking_result = self.prepare_booking(user_input)

#             if booking_result.get("success"):

#                 booking = booking_result["booking"]


            

#                 try:

#                     car = Car.objects.get(
#                     id=booking["car_id"]
#                 )

#                 except Car.DoesNotExist:

#                     return {
#                     "success": False,
#                     "tool_used": True,
#                     "error": "Car not found.",
#                 }


            
#                 is_staff_role = self.user.groups.filter(
#                 name__in=["Admin", "Manager"]).exists()


#                 if not is_staff_role and car.owner != self.user:

#                     return {
#                     "success": False,
#                     "tool_used": True,
#                     "error": (
#                         "You do not have permission "
#                         "to book an appointment for this car."
#                     ),
#                 }


            

#                 slot_result = self.execute_function_call(
#                 "check_appointment_slot",
#                 {
#                     "technician_id": booking["technician_id"],
#                     "appointment_date": booking["appointment_date"],
#                     "appointment_time": booking["appointment_time"],
#                 },
#             )


#                 if not slot_result["success"]:

#                     return {
#                     "success": False,
#                     "tool_used": True,
#                     "function_name": "check_appointment_slot",
#                     "error": slot_result.get(
#                         "message",
#                         "Could not check appointment availability.",
#                     ),
#                 }


#                 tool_result = slot_result["result"]


            

#                 if not tool_result.get("available"):

#                     return {
#                     "success": True,
#                     "tool_used": True,
#                     "function_name": "check_appointment_slot",
#                     "tool_result": tool_result,
#                     "confirmation_required": False,
#                     "answer": (
#                         "The appointment slot is not available.\n\n"
#                         f"Reason: "
#                         f"{tool_result.get('reason', 'Unknown reason.')}"
#                     ),
#                 }

#                 self.set_pending_booking(booking)


#                 return {
#                 "success": True,
#                 "tool_used": True,
#                 "function_name": "check_appointment_slot",
#                 "tool_result": tool_result,
#                 "confirmation_required": True,
#                 "next_action": "book_appointment",
#                 "pending_action": self.pending_action,
#                 "message": (
#                     "The appointment slot is available.\n\n"
#                     f"Car: {car.brand} {car.model}\n"
#                     f"Car ID: {booking['car_id']}\n"
#                     f"Technician: "
#                     f"{tool_result['technician']['name']}\n"
#                     f"Specialization: "
#                     f"{tool_result['technician']['specialization']}\n"
#                     f"Service: {booking['service_type']}\n"
#                     f"Date: {booking['appointment_date']}\n"
#                     f"Time: {booking['appointment_time']}\n\n"
#                     "Do you confirm this appointment?"
#                 ),
#             }

#         # Handle maintenance history for "my car"
#         maintenance_keywords = [
#     "maintenance history",
#     "maintenance records",
#     "service history",
# ]

#         if any(keyword in user_input.lower() for keyword in maintenance_keywords):
#             try:
#                 cars_result = self.execute_function_call("get_my_cars",{},)

#                 if not cars_result["success"]:
#                     return {
#                 "success": False,
#                 "tool_used": True,
#                 "function_name": "get_my_cars",
#                 "error": cars_result.get(
#                     "message",
#                     "Could not retrieve your cars.",
#                 ),
#             }

#                 cars = cars_result["result"].get("cars", [])

#                 if not cars:
#                     return {
#                 "success": True,
#                 "tool_used": True,
#                 "function_name": "get_my_cars",
#                 "answer": "You do not have any cars registered yet.",
#             }

#                 if len(cars) == 1:
#                     car = cars[0]
                    
#                     history_result = self.execute_function_call("get_maintenance_history",{
#                     "car_id": car["id"],},)

#                     if not history_result["success"]:
#                         return {
#                             "success": False,
#                             "tool_used": True,
#                             "function_name": "get_maintenance_history",
#                             "error": history_result.get("message",
#                                     "Could not retrieve maintenance history.",),}

#                     history = history_result["result"]

#                     if history["maintenance_count"] == 0:
#                         answer = (f"Your {history['car']} has no maintenance records yet.")
#                     else:
#                                 answer = (f"Here is the maintenance history for your "
#                                         f"{history['car']}:\n\n")

#                                 for record in history["maintenance_history"]:
#                                     answer += (
#                                         f"• Service: {record['service_type']}\n"
#                                         f"  Date: {record['service_date']}\n"
#                                         f"  Mileage: {record['mileage']} km\n"
#                                         f"  Cost: {record['cost']}\n"
#                                         f"  Status: {record['status']}\n"
#                                         f"  Technician: {record['technician']}\n\n")

#                     return {
#                             "success": True,
#                             "tool_used": True,
#                             "function_name": "get_maintenance_history",
#                             "answer": answer,}

#             #         history_result = self.execute_function_call(
#             #     "get_maintenance_history",
#             #     {
#             #         "car_id": car["id"],
#             #     },
#             # )

#             #         if not history_result["success"]:
#             #             return {
#             #         "success": False,
#             #         "tool_used": True,
#             #         "function_name": "get_maintenance_history",
#             #         "error": history_result.get(
#             #             "message",
#             #             "Could not retrieve maintenance history.",
#             #         ),
#             #     }

#             #         return {
#             #     "success": True,
#             #     "tool_used": True,
#             #     "function_name": "get_maintenance_history",
#             #     "answer": history_result["result"],
#             # }

#                 car_list = "\n".join(
#             [
#                     f"{index}. {car['brand']} {car['model']} "
#                     f"({car['license_plate']})"
#                     for index, car in enumerate(cars, start=1)
#             ]
#         )

#                 return {
#             "success": True,
#             "tool_used": True,
#             "function_name": "get_my_cars",
#             "answer": (
#                 "You have multiple cars registered:\n\n"
#                 f"{car_list}\n\n"
#                 "Please tell me which car you want to check."
#             ),
#         }

#             except ValidationError as exc:
#                 return {
#             "success": False,
#             "tool_used": True,
#             "error": str(exc),
#         }

#     #     response = self.client.models.generate_content(
#     #     model="gemini-3.5-flash-lite",
#     #     contents=user_input,
#     #     config=types.GenerateContentConfig(
#     #         tools=[
#     #             types.Tool(
#     #                 function_declarations=self.function_declarations
#     #             )
#     #         ],
#     #         automatic_function_calling=types.AutomaticFunctionCallingConfig(
#     #             disable=True
#     #         ),
#     #     ),
#     # )
    
#     #     try:
#     #        response = self.client.models.generate_content(
#     #        model="gemini-3.5-flash-lite",
#     #        contents=user_input,
#     #        config=types.GenerateContentConfig(
#     #         tools=[
#     #             types.Tool(
#     #                 function_declarations=self.function_declarations
#     #             )
#     #         ],
#     #         automatic_function_calling=types.AutomaticFunctionCallingConfig(
#     #             disable=True
#     #         ),
#     #     ),
#     # )

#     #     except Exception as exc:
#     #         error_message = str(exc)

#     #         if "503" in error_message or "UNAVAILABLE" in error_message:
#     #             return {
#     #         "success": False,
#     #         "tool_used": False,
#     #         "error": "AI service is temporarily unavailable. Please try again in a moment.",
#     #     }

#     #         raise  
#         response = None

#         for attempt in range(3):
#             try:
#                 response = self.client.models.generate_content(
#                 model="gemini-3.5-flash-lite",
#                 contents=user_input,
#                 config=types.GenerateContentConfig(
#                 tools=[
#                     types.Tool(
#                         function_declarations=self.function_declarations
#                     )
#                 ],
#                 automatic_function_calling=types.AutomaticFunctionCallingConfig(
#                     disable=True
#                 ),
#             ),
#         )

#                 break

#             except errors.ServerError as exc:
#                 error_message = str(exc)

#                 if "503" not in error_message and "UNAVAILABLE" not in error_message:
#                     raise

#                 if attempt == 2:
#                     return {
#                 "success": False,
#                 "tool_used": False,
#                 "error": (
#                     "The AI service is temporarily unavailable. "
#                     "Please try again in a moment."
#                 ),
#             }

#                 time.sleep(2 ** attempt)



#         if not response.function_calls:

#             return {
#             "success": True,
#             "tool_used": False,
#             "answer": response.text,
#         }


#         function_call = response.function_calls[0]

#         function_name = function_call.name

#         arguments = dict(function_call.args)



#         if function_name == "check_appointment_slot":

#             execution = self.execute_function_call(
#             function_name,
#             arguments,
#         )


#             if not execution["success"]:

#                 return {
#                 "success": False,
#                 "tool_used": True,
#                 "function_name": function_name,
#                 "arguments": arguments,
#                 "error": execution.get(
#                     "message",
#                     "Could not check the appointment slot.",
#                 ),
#             }


#             tool_result = execution["result"]


#             if tool_result.get("available") is True:

#                 return {
#                 "success": True,
#                 "tool_used": True,
#                 "function_name": function_name,
#                 "arguments": arguments,
#                 "tool_result": tool_result,
#                 "confirmation_required": False,
#                 "answer": (
#                     "The appointment slot is available.\n\n"
#                     f"Technician: "
#                     f"{tool_result['technician']['name']}\n"
#                     f"Specialization: "
#                     f"{tool_result['technician']['specialization']}\n"
#                     f"Date: "
#                     f"{tool_result['appointment_date']}\n"
#                     f"Time: "
#                     f"{tool_result['appointment_time']}"
#                 ),
#             }


#             return {
#             "success": True,
#             "tool_used": True,
#             "function_name": function_name,
#             "arguments": arguments,
#             "tool_result": tool_result,
#             "confirmation_required": False,
#             "answer": (
#                 "The appointment slot is not available.\n\n"
#                 f"Reason: "
#                 f"{tool_result.get('reason', 'Unknown reason.')}"
#             ),
#         }


   

#         if function_name == "book_appointment":

#             return self.build_confirmation_request(
#             function_name,
#             arguments,
#         )


    

#         execution = self.execute_function_call(
#         function_name,
#         arguments,)


#         if not execution["success"]:

#             return {
#             "success": False,
#             "tool_used": True,
#             "function_name": function_name,
#             "arguments": arguments,
#             "error": execution.get(
#                 "message",
#                 "Tool execution failed.",
#             ),
#         }


#         tool_result = execution["result"]


    
#         final_prompt = f"""
# You are a Smart Car Service Assistant.

# The user asked:
# {user_input}

# The backend tool that was executed:
# {function_name}

# Tool result:
# {tool_result}

# Answer the user clearly and concisely.

# Do not invent information.
# Only use information contained in the tool result.
# """


#         final_response = self.client.models.generate_content(
#         model="gemini-3.5-flash-lite",
#         contents=final_prompt,
#     )


#         return {
#         "success": True,
#         "tool_used": True,
#         "function_name": function_name,
#         "arguments": arguments,
#         "tool_result": tool_result,
#         "answer": final_response.text,
#     }

                
        
#     def requires_confirmation(self, function_name):
#         """
#         Return True for tools that perform actions
#         that modify system data.
#         """
#         confirmation_required_tools = {
#             "book_appointment",
#         }

#         return function_name in confirmation_required_tools   
    
#     def build_confirmation_request(self, function_name, arguments):
#         """
#         Build a human-readable confirmation request
#         before executing a destructive or state-changing action.
#         """

#         if function_name == "book_appointment":
#             return {
#                 "confirmation_required": True,
#                 "function_name": function_name,
#                 "message": (
#                     "Please confirm the following appointment:\n"
#                     f"- Car ID: {arguments.get('car_id')}\n"
#                     f"- Technician ID: {arguments.get('technician_id')}\n"
#                     f"- Service: {arguments.get('service_type')}\n"
#                     f"- Date: {arguments.get('appointment_date')}\n"
#                     f"- Time: {arguments.get('appointment_time')}\n"
#                     f"- Notes: {arguments.get('notes', '')}\n\n"
#                     "Do you confirm this appointment?"
#                 ),
#             }

#         return {
#             "confirmation_required": False,
#         } 
        
#     def prepare_booking(self, user_input):
#         """
#         Extract all information required for a booking
#         without executing the booking.
#         """

#         response = self.client.models.generate_content(
#             model="gemini-3.5-flash-lite",
#             contents=f"""
# Extract the appointment booking information from the user's request.

# User request:
# {user_input}

# Return ONLY valid JSON with this structure:

# {{
#     "car_id": integer,
#     "technician_id": integer,
#     "service_type": "string",
#     "appointment_date": "YYYY-MM-DD",
#     "appointment_time": "HH:MM",
#     "notes": "string"
# }}

# Do not invent missing values.
# If a value is not provided, use null.
# """,
#         )

#         import json

#         try:
#             data = json.loads(response.text)
#         except json.JSONDecodeError:
#             return {
#                 "success": False,
#                 "message": "Could not extract valid booking information."
#             }

#         required_fields = [
#             "car_id",
#             "technician_id",
#             "service_type",
#             "appointment_date",
#             "appointment_time",
#         ]

#         missing_fields = [
#             field
#             for field in required_fields
#             if not data.get(field)
#         ]

#         if missing_fields:
#             return {
#                 "success": False,
#                 "message": "Missing booking information.",
#                 "missing_fields": missing_fields,
#             }

#         return {
#             "success": True,
#             "booking": data,
#         }    
        
#     def set_pending_booking(self, booking):
#         """
#         Store a validated booking request waiting for user confirmation.
#         """
#         self.pending_action = {
#         "function_name": "book_appointment",
#         "arguments": {
#             "car_id": booking["car_id"],
#             "technician_id": booking["technician_id"],
#             "service_type": booking["service_type"],
#             "appointment_date": booking["appointment_date"],
#             "appointment_time": booking["appointment_time"],
#             "notes": booking.get("notes") or "",
#         },
#     }

#         return self.pending_action 
    
#     def confirm_pending_action(self, confirmed):
#         """
#         Execute the pending action only after explicit confirmation.
#         """

#         if not confirmed:
#             self.pending_action = None

#             return {
#                 "success": False,
#                 "confirmed": False,
#                 "message": "Appointment booking was cancelled."
#             }

#         if not self.pending_action:
#             return {
#                 "success": False,
#                 "confirmed": False,
#                 "message": "There is no pending action to confirm."
#             }

#         function_name = self.pending_action["function_name"]
#         arguments = self.pending_action["arguments"]

#         execution = self.execute_function_call(
#             function_name,
#             arguments,
#         )

#         if not execution["success"]:
#             return {
#                 "success": False,
#                 "confirmed": True,
#                 "message": execution.get(
#                     "message",
#                     "The appointment could not be booked."
#                 ),
#             }

#         self.pending_action = None

#         return {
#             "success": True,
#             "confirmed": True,
#             "function_name": function_name,
#             "result": execution["result"],
#         }   


# import json
# from django.core.exceptions import ValidationError
# from google import genai
# from google.genai import types
# from django.conf import settings
# from datetime import date, time, datetime
# from .tools import (
#     get_maintenance_history,
#     find_available_technicians,
#     check_appointment_slot,
#     book_appointment,
#     find_low_stock_spare_parts)
# from cars.models import Car


# class SmartCarAgent:
#     """
#     Smart Car Agent.

#     Flow:
#     User Input
#         ↓
#     LLM Reasoning
#         ↓
#     Tool Selection
#         ↓
#     Parameter Validation
#         ↓
#     Tool Execution
#         ↓
#     Observation
#         ↓
#     Final Response
#     """

#     def __init__(self, user):
#         self.user = user

#         self.client = genai.Client(
#             api_key=settings.GEMINI_API_KEY
#         )
        
#         self.pending_action = None

#         self.tools = {
#             "get_maintenance_history": get_maintenance_history,
#             "find_available_technicians": find_available_technicians,
#             "check_appointment_slot": check_appointment_slot,
#             "book_appointment": book_appointment,
#             "find_low_stock_spare_parts": find_low_stock_spare_parts,
#         }
        
#         self.function_declarations = [
#             types.FunctionDeclaration(
#         name="get_maintenance_history",
#         description="Get the maintenance history of a specific car.",
#         parameters=types.Schema(
#             type="OBJECT",
#             properties={
#                 "car_id": types.Schema(
#                     type="INTEGER",
#                     description="The ID of the car."
#                 )
#             },
#             required=["car_id"],
#         ),
#     ),

#             types.FunctionDeclaration(
#         name="find_available_technicians",
#         description="Find technicians who are currently available.",
#         parameters=types.Schema(
#             type="OBJECT",
#             properties={},
#         ),
#     ),

#             types.FunctionDeclaration(
#     name="check_appointment_slot",
#     description="Check whether a technician appointment slot is available.",
#     parameters=types.Schema(
#         type="OBJECT",
#         properties={
#             "technician_id": types.Schema(
#                 type="INTEGER",
#                 description="The technician ID."
#             ),
#             "appointment_date": types.Schema(
#                 type="STRING",
#                 description="Appointment date in YYYY-MM-DD format."
#             ),
#             "appointment_time": types.Schema(
#                 type="STRING",
#                 description="Appointment time in HH:MM format."
#             ),
#         },
#         required=[
#             "technician_id",
#             "appointment_date",
#             "appointment_time",
#         ],
#     ),
# ),

#             types.FunctionDeclaration(
#         name="book_appointment",
#         description="Book a service appointment for a user's car.",
#         parameters=types.Schema(
#             type="OBJECT",
#             properties={
#                 "car_id": types.Schema(
#                     type="INTEGER",
#                     description="The user's car ID."
#                 ),
#                 "technician_id": types.Schema(
#                     type="INTEGER",
#                     description="The technician ID."
#                 ),
#                 "service_type": types.Schema(
#                     type="STRING",
#                     description="Type of service requested."
#                 ),
#                 "appointment_date": types.Schema(
#                     type="STRING",
#                     description="Appointment date in YYYY-MM-DD format."
#                 ),
#                 "appointment_time": types.Schema(
#                     type="STRING",
#                     description="Appointment time in HH:MM format."
#                 ),
#                 "notes": types.Schema(
#                     type="STRING",
#                     description="Optional appointment notes."
#                 ),
#             },
#             required=[
#                 "car_id",
#                 "technician_id",
#                 "service_type",
#                 "appointment_date",
#                 "appointment_time",
#             ],
#         ),
#     ),
#             types.FunctionDeclaration(
#     name="find_low_stock_spare_parts",
#     description="Find spare parts whose stock quantity is at or below the minimum stock level.",
#     parameters=types.Schema(
#         type="OBJECT",
#         properties={},
#     ),
# ),
# ]

#     def perceive_goal(self, user_input):
#         """
#         Ask the LLM to understand the user's goal.
#         """

#         prompt = f"""
# You are the reasoning component of a Smart Car Service system.

# Analyze the user's request and return ONLY valid JSON.

# Available goals:

# 1. maintenance_history
# 2. available_technicians
# 3. appointment
# 4. unknown

# User request:
# {user_input}

# Return exactly:

# {{
#     "goal": "one of the available goals",
#     "reason": "short explanation"
# }}
# """

#         response = self.client.models.generate_content(
#             model="gemini-3.5-flash-lite",
#             contents=prompt,
#         )

#         try:
#             return json.loads(response.text)
#         except json.JSONDecodeError:
#             return {
#                 "goal": "unknown",
#                 "reason": "The model returned invalid JSON.",
#             }

#     def select_tool(self, goal):
#         """
#         Map the goal to an approved backend tool.
#         """

#         goal_to_tool = {
#             "maintenance_history": "get_maintenance_history",
#             "available_technicians": "find_available_technicians",
#             "appointment": "book_appointment",
#         }

#         tool_name = goal_to_tool.get(goal)

#         if not tool_name:
#             return None

#         return self.tools.get(tool_name)

#     def extract_parameters(self, goal, user_input):
#         """
#         Extract parameters from the user's request.

#         This stage currently returns only the parameters
#         that can safely be inferred from the conversation.
#         """

#         prompt = f"""
# You are extracting parameters for a Smart Car Service system.

# User request:
# {user_input}

# Detected goal:
# {goal}

# Return ONLY valid JSON.

# For maintenance_history:
# {{
#     "car_id": null
# }}

# For available_technicians:
# {{}}

# For appointment:
# {{
#     "car_id": null,
#     "technician_id": null,
#     "service_type": null,
#     "appointment_date": null,
#     "appointment_time": null,
#     "notes": ""
# }}
# """

#         response = self.client.models.generate_content(
#             model="gemini-3.5-flash-lite",
#             contents=prompt,
#         )

#         try:
#             return json.loads(response.text)
#         except json.JSONDecodeError:
#             raise ValidationError(
#                 "The AI returned invalid parameters."
#             )

#     def execute_tool(self, tool, parameters):
#         """
#         Execute only an approved backend tool.
#         """

#         if tool is None:
#             return {
#                 "success": False,
#                 "message": "No suitable tool was found.",
#             }

#         return tool(
#             user=self.user,
#             **parameters,
#         )

#     def observe(self, result):
#         """
#         Observe the tool result.
#         """

#         return result

#     def complete(self, observation):
#         """
#         Return the final result.
#         """

#         return observation

#     def run(self, user_input):
#         """
#         Execute the complete Agentic AI pipeline.
#         """

#         perception = self.perceive_goal(user_input)

#         goal = perception.get("goal", "unknown")

#         if goal == "unknown":
#             return {
#                 "success": False,
#                 "message": "I could not determine what you want to do.",
#             }

#         tool = self.select_tool(goal)

#         if tool is None:
#             return {
#                 "success": False,
#                 "message": "No suitable tool is available.",
#             }

#         parameters = self.extract_parameters(
#             goal,
#             user_input,
#         )

#         result = self.execute_tool(
#             tool,
#             parameters,
#         )

#         observation = self.observe(result)

#         return self.complete(observation)
    
#     def choose_function(self, user_input):
#         """
#         Ask Gemini to choose one approved backend function.
#         Gemini does not execute the function.
#         """

#         response = self.client.models.generate_content(
#             model="gemini-3.5-flash-lite",
#             contents=user_input,
#             config=types.GenerateContentConfig(
#             tools=[
#                 types.Tool(
#                     function_declarations=self.function_declarations
#                 )
#             ],
#             automatic_function_calling=types.AutomaticFunctionCallingConfig(
#                 disable=True
#             ),
#         ),
#     )

#         if not response.function_calls:
#             return {
#             "function_name": None,
#             "arguments": {},
#             "text": response.text,
#         }

#         function_call = response.function_calls[0]

#         return {
#         "function_name": function_call.name,
#         "arguments": dict(function_call.args),
#     }
        
#     def execute_function_call(self, function_name, arguments):
#         """
#         Execute only functions that are explicitly registered
#         in the Agent's tool whitelist.
#         """

#         if not function_name:
#             return {
#             "success": False,
#             "message": "No function was requested.",
#         }

#         tool = self.tools.get(function_name)

#         if tool is None:
#             return {
#             "success": False,
#             "message": "Requested function is not allowed.",
#         }

#         try:
#             result = tool(
#             user=self.user,
#             **arguments,
#         )

#             return {
#             "success": True,
#             "function_name": function_name,
#             "result": result,
#         }

#         except ValidationError as exc:
#             return {
#             "success": False,
#             "function_name": function_name,
#             "message": str(exc),
#         }    
            
#     # def run_agent_loop(self, user_input):
#     #     """
#     #     Full Agentic AI loop.

#     #     Gemini decides whether a backend tool is needed.
#     #     The Agent executes only approved tools.
#     #     The tool result is then returned to Gemini
#     #     to generate the final natural-language response.
#     #     """

#     #     response = self.client.models.generate_content(
#     #         model="gemini-3.5-flash-lite",
#     #         contents=user_input,
#     #         config=types.GenerateContentConfig(
#     #         tools=[
#     #             types.Tool(
#     #                 function_declarations=self.function_declarations
#     #             )
#     #         ],
#     #         automatic_function_calling=types.AutomaticFunctionCallingConfig(
#     #             disable=True
#     #         ),
#     #     ),
#     # )

#     #     if not response.function_calls:
#     #         return {
#     #         "success": True,
#     #         "tool_used": False,
#     #         "answer": response.text,
#     #     }

#     #     function_call = response.function_calls[0]

#     #     function_name = function_call.name
#     #     arguments = dict(function_call.args)

#     #     execution = self.execute_function_call(
#     #     function_name,
#     #     arguments,
#     # )

#     #     return {
#     #     "success": execution["success"],
#     #     "tool_used": True,
#     #     "function_name": function_name,
#     #     "arguments": arguments,
#     #     "tool_result": execution,
#     # }        
    
# #     def run_agent_loop(self, user_input):
# #         """
# #         Full Agentic AI loop.

# #         Flow:
# #         User Input
# #         -> Gemini Tool Selection
# #         -> Approved Tool Execution
# #         -> Tool Result
# #         -> Gemini Final Answer
# #         """

# #         response = self.client.models.generate_content(
# #             model="gemini-3.5-flash-lite",
# #             contents=user_input,
# #             config=types.GenerateContentConfig(
# #                 tools=[
# #                     types.Tool(
# #                         function_declarations=self.function_declarations
# #                     )
# #                 ],
# #                 automatic_function_calling=types.AutomaticFunctionCallingConfig(
# #                     disable=True
# #                 ),
# #             ),
# #         )

      
# #         if not response.function_calls:
# #             return {
# #                 "success": True,
# #                 "tool_used": False,
# #                 "answer": response.text,
# #             }


# #         function_call = response.function_calls[0]

# #         function_name = function_call.name
# #         arguments = dict(function_call.args)

        
# #         if self.requires_confirmation(function_name):
# #             return self.build_confirmation_request(
# #                 function_name,
# #                 arguments,)
            
# #         execution = self.execute_function_call(
# #             function_name,
# #             arguments,)

# #         if not execution["success"]:
# #             return {
# #                 "success": False,
# #                 "tool_used": True,
# #                 "function_name": function_name,
# #                 "arguments": arguments,
# #                 "error": execution.get(
# #                     "message",
# #                     "Tool execution failed."
# #                 ),
# #             }


# #         tool_result = execution["result"]

# #         # if function_name == "check_appointment_slot":
# #         #     if tool_result.get("available") is True:
# #         #         return {
# #         #             "success": True,
# #         #             "tool_used": True,
# #         #             "function_name": function_name,
# #         #             "arguments": arguments,
# #         #             "tool_result": tool_result,
# #         #             "confirmation_required": True,
# #         #             "next_action": "book_appointment",
# #         #             "message": (
# #         #                 "The appointment slot is available.\n\n"
# #         #                 "Please confirm the following appointment:\n"
# #         #                 f"- Technician: {tool_result['technician']['name']}\n"
# #         #                 f"- Specialization: {tool_result['technician']['specialization']}\n"
# #         #                 f"- Date: {tool_result['appointment_date']}\n"
# #         #                 f"- Time: {tool_result['appointment_time']}\n\n"
# #         #                 "Do you confirm this appointment?"
# #         #             ),
# #         #         }
# #         if function_name == "check_appointment_slot":
# #             if tool_result.get("available") is True:

# #                 self.pending_action = {
# #                     "function_name": "book_appointment",
# #                     "arguments": {
# #                         "car_id": arguments.get("car_id"),
# #                         "technician_id": arguments.get("technician_id"),
# #                         "service_type": arguments.get("service_type"),
# #                         "appointment_date": arguments.get("appointment_date"),
# #                         "appointment_time": arguments.get("appointment_time"),
# #                         "notes": arguments.get("notes", ""),
# #                     },
# #                 }

# #                 return {
# #                     "success": True,
# #                     "tool_used": True,
# #                     "function_name": function_name,
# #                     "arguments": arguments,
# #                     "tool_result": tool_result,
# #                     "confirmation_required": True,
# #                     "next_action": "book_appointment",
# #                     "message": (
# #                         "The appointment slot is available.\n\n"
# #                         "Please confirm the following appointment:\n"
# #                         f"- Car ID: {arguments.get('car_id')}\n"
# #                         f"- Technician: {tool_result['technician']['name']}\n"
# #                         f"- Specialization: {tool_result['technician']['specialization']}\n"
# #                         f"- Service: {arguments.get('service_type')}\n"
# #                         f"- Date: {tool_result['appointment_date']}\n"
# #                         f"- Time: {tool_result['appointment_time']}\n\n"
# #                         "Do you confirm this appointment?"
# #                     )
# #                 }
                
# #         final_prompt = f"""
# # You are the final response generator for a Smart Car Service System.

# # The user asked:
# # {user_input}

# # The backend tool that was executed:
# # {function_name}

# # The tool result is:
# # {tool_result}

# # Using only the tool result, provide a clear and concise
# # answer to the user.

# # Do not invent information.
# # Do not mention internal tools, function calling,
# # database, ORM, or implementation details.
# # """

# #         final_response = self.client.models.generate_content(
# #             model="gemini-3.5-flash-lite",
# #             contents=final_prompt,
# #         )


# #         return {
# #             "success": True,
# #             "tool_used": True,
# #             "function_name": function_name,
# #             "arguments": arguments,
# #             "tool_result": tool_result,
# #             "answer": final_response.text,
# #         }

#     def run_agent_loop(self, user_input):


#         if self.pending_action:

#             confirmation = user_input.strip().lower()

#             if confirmation in [
#             "yes",
#             "y",
#             "confirm",
#             "confirmed",
#             "approve",
#             "ok",
#             "okay",
#         ]:

#                 result = self.confirm_pending_action(True)

#                 if result["success"]:

#                     appointment = result["result"]["appointment"]

#                     return {
#                     "success": True,
#                     "tool_used": True,
#                     "function_name": "book_appointment",
#                     "confirmation_required": False,
#                     "answer": (
#                         "Appointment booked successfully.\n\n"
#                         f"Car: {appointment['car']}\n"
#                         f"Technician: {appointment['technician']}\n"
#                         f"Service: {appointment['service_type']}\n"
#                         f"Date: {appointment['appointment_date']}\n"
#                         f"Time: {appointment['appointment_time']}\n"
#                         f"Status: {appointment['status']}"
#                     ),
#                 }

#                 return {
#                 "success": False,
#                 "tool_used": True,
#                 "function_name": "book_appointment",
#                 "confirmation_required": False,
#                 "error": result.get(
#                     "message",
#                     "The appointment could not be booked.",
#                 ),
#             }


#             if confirmation in [
#             "no",
#             "n",
#             "cancel",
#             "cancelled",
#             "decline",
#             "reject",
#         ]:

#                     result = self.confirm_pending_action(False)

#                     return {
#                 "success": True,
#                 "tool_used": False,
#                 "confirmation_required": False,
#                 "answer": result["message"],
#             }


#             return {
#             "success": True,
#             "tool_used": False,
#             "confirmation_required": True,
#             "pending_action": self.pending_action,
#             "message": (
#                 "I have a pending appointment booking.\n\n"
#                 "Please reply with Yes to confirm or No to cancel."
#             ),
#         }


    

#         booking_keywords = [
#         "book",
#         "booking",
#         "appointment",
#         "schedule",
#         "reserve",
#     ]

#         is_booking_request = any(
#         keyword in user_input.lower()
#         for keyword in booking_keywords
#     )


    

#         if is_booking_request:

#             booking_result = self.prepare_booking(user_input)

#             if booking_result.get("success"):

#                 booking = booking_result["booking"]


            

#                 try:

#                     car = Car.objects.get(
#                     id=booking["car_id"]
#                 )

#                 except Car.DoesNotExist:

#                     return {
#                     "success": False,
#                     "tool_used": True,
#                     "error": "Car not found.",
#                 }


            
#                 is_staff_role = self.user.groups.filter(
#                 name__in=["Admin", "Manager"]).exists()


#                 if not is_staff_role and car.owner != self.user:

#                     return {
#                     "success": False,
#                     "tool_used": True,
#                     "error": (
#                         "You do not have permission "
#                         "to book an appointment for this car."
#                     ),
#                 }


            

#                 slot_result = self.execute_function_call(
#                 "check_appointment_slot",
#                 {
#                     "technician_id": booking["technician_id"],
#                     "appointment_date": booking["appointment_date"],
#                     "appointment_time": booking["appointment_time"],
#                 },
#             )


#                 if not slot_result["success"]:

#                     return {
#                     "success": False,
#                     "tool_used": True,
#                     "function_name": "check_appointment_slot",
#                     "error": slot_result.get(
#                         "message",
#                         "Could not check appointment availability.",
#                     ),
#                 }


#                 tool_result = slot_result["result"]


            

#                 if not tool_result.get("available"):

#                     return {
#                     "success": True,
#                     "tool_used": True,
#                     "function_name": "check_appointment_slot",
#                     "tool_result": tool_result,
#                     "confirmation_required": False,
#                     "answer": (
#                         "The appointment slot is not available.\n\n"
#                         f"Reason: "
#                         f"{tool_result.get('reason', 'Unknown reason.')}"
#                     ),
#                 }

#                 self.set_pending_booking(booking)


#                 return {
#                 "success": True,
#                 "tool_used": True,
#                 "function_name": "check_appointment_slot",
#                 "tool_result": tool_result,
#                 "confirmation_required": True,
#                 "next_action": "book_appointment",
#                 "pending_action": self.pending_action,
#                 "message": (
#                     "The appointment slot is available.\n\n"
#                     f"Car: {car.brand} {car.model}\n"
#                     f"Car ID: {booking['car_id']}\n"
#                     f"Technician: "
#                     f"{tool_result['technician']['name']}\n"
#                     f"Specialization: "
#                     f"{tool_result['technician']['specialization']}\n"
#                     f"Service: {booking['service_type']}\n"
#                     f"Date: {booking['appointment_date']}\n"
#                     f"Time: {booking['appointment_time']}\n\n"
#                     "Do you confirm this appointment?"
#                 ),
#             }


#     # ============================================================
#     # 4. Normal AI / Tool Selection
#     # ============================================================

#         response = self.client.models.generate_content(
#         model="gemini-3.5-flash-lite",
#         contents=user_input,
#         config=types.GenerateContentConfig(
#             tools=[
#                 types.Tool(
#                     function_declarations=self.function_declarations
#                 )
#             ],
#             automatic_function_calling=types.AutomaticFunctionCallingConfig(
#                 disable=True
#             ),
#         ),
#     )




#         if not response.function_calls:

#             return {
#             "success": True,
#             "tool_used": False,
#             "answer": response.text,
#         }


#         function_call = response.function_calls[0]

#         function_name = function_call.name

#         arguments = dict(function_call.args)



#         if function_name == "check_appointment_slot":

#             execution = self.execute_function_call(
#             function_name,
#             arguments,
#         )


#             if not execution["success"]:

#                 return {
#                 "success": False,
#                 "tool_used": True,
#                 "function_name": function_name,
#                 "arguments": arguments,
#                 "error": execution.get(
#                     "message",
#                     "Could not check the appointment slot.",
#                 ),
#             }


#             tool_result = execution["result"]


#             if tool_result.get("available") is True:

#                 return {
#                 "success": True,
#                 "tool_used": True,
#                 "function_name": function_name,
#                 "arguments": arguments,
#                 "tool_result": tool_result,
#                 "confirmation_required": False,
#                 "answer": (
#                     "The appointment slot is available.\n\n"
#                     f"Technician: "
#                     f"{tool_result['technician']['name']}\n"
#                     f"Specialization: "
#                     f"{tool_result['technician']['specialization']}\n"
#                     f"Date: "
#                     f"{tool_result['appointment_date']}\n"
#                     f"Time: "
#                     f"{tool_result['appointment_time']}"
#                 ),
#             }


#             return {
#             "success": True,
#             "tool_used": True,
#             "function_name": function_name,
#             "arguments": arguments,
#             "tool_result": tool_result,
#             "confirmation_required": False,
#             "answer": (
#                 "The appointment slot is not available.\n\n"
#                 f"Reason: "
#                 f"{tool_result.get('reason', 'Unknown reason.')}"
#             ),
#         }


   

#         if function_name == "book_appointment":

#             return self.build_confirmation_request(
#             function_name,
#             arguments,
#         )


    

#         execution = self.execute_function_call(
#         function_name,
#         arguments,)


#         if not execution["success"]:

#             return {
#             "success": False,
#             "tool_used": True,
#             "function_name": function_name,
#             "arguments": arguments,
#             "error": execution.get(
#                 "message",
#                 "Tool execution failed.",
#             ),
#         }


#         tool_result = execution["result"]


    
#         final_prompt = f"""
# You are a Smart Car Service Assistant.

# The user asked:
# {user_input}

# The backend tool that was executed:
# {function_name}

# Tool result:
# {tool_result}

# Answer the user clearly and concisely.

# Do not invent information.
# Only use information contained in the tool result.
# """


#         final_response = self.client.models.generate_content(
#         model="gemini-3.5-flash-lite",
#         contents=final_prompt,
#     )


#         return {
#         "success": True,
#         "tool_used": True,
#         "function_name": function_name,
#         "arguments": arguments,
#         "tool_result": tool_result,
#         "answer": final_response.text,
#     }

                
        
#     def requires_confirmation(self, function_name):
#         """
#         Return True for tools that perform actions
#         that modify system data.
#         """
#         confirmation_required_tools = {
#             "book_appointment",
#         }

#         return function_name in confirmation_required_tools   
    
#     def build_confirmation_request(self, function_name, arguments):
#         """
#         Build a human-readable confirmation request
#         before executing a destructive or state-changing action.
#         """

#         if function_name == "book_appointment":
#             return {
#                 "confirmation_required": True,
#                 "function_name": function_name,
#                 "message": (
#                     "Please confirm the following appointment:\n"
#                     f"- Car ID: {arguments.get('car_id')}\n"
#                     f"- Technician ID: {arguments.get('technician_id')}\n"
#                     f"- Service: {arguments.get('service_type')}\n"
#                     f"- Date: {arguments.get('appointment_date')}\n"
#                     f"- Time: {arguments.get('appointment_time')}\n"
#                     f"- Notes: {arguments.get('notes', '')}\n\n"
#                     "Do you confirm this appointment?"
#                 ),
#             }

#         return {
#             "confirmation_required": False,
#         } 
        
#     def prepare_booking(self, user_input):
#         """
#         Extract all information required for a booking
#         without executing the booking.
#         """

#         response = self.client.models.generate_content(
#             model="gemini-3.5-flash-lite",
#             contents=f"""
# Extract the appointment booking information from the user's request.

# User request:
# {user_input}

# Return ONLY valid JSON with this structure:

# {{
#     "car_id": integer,
#     "technician_id": integer,
#     "service_type": "string",
#     "appointment_date": "YYYY-MM-DD",
#     "appointment_time": "HH:MM",
#     "notes": "string"
# }}

# Do not invent missing values.
# If a value is not provided, use null.
# """,
#         )

#         import json

#         try:
#             data = json.loads(response.text)
#         except json.JSONDecodeError:
#             return {
#                 "success": False,
#                 "message": "Could not extract valid booking information."
#             }

#         required_fields = [
#             "car_id",
#             "technician_id",
#             "service_type",
#             "appointment_date",
#             "appointment_time",
#         ]

#         missing_fields = [
#             field
#             for field in required_fields
#             if not data.get(field)
#         ]

#         if missing_fields:
#             return {
#                 "success": False,
#                 "message": "Missing booking information.",
#                 "missing_fields": missing_fields,
#             }

#         return {
#             "success": True,
#             "booking": data,
#         }    
        
#     def set_pending_booking(self, booking):
#         """
#         Store a validated booking request waiting for user confirmation.
#         """
#         self.pending_action = {
#         "function_name": "book_appointment",
#         "arguments": {
#             "car_id": booking["car_id"],
#             "technician_id": booking["technician_id"],
#             "service_type": booking["service_type"],
#             "appointment_date": booking["appointment_date"],
#             "appointment_time": booking["appointment_time"],
#             "notes": booking.get("notes") or "",
#         },
#     }

#         return self.pending_action 
    
#     def confirm_pending_action(self, confirmed):
#         """
#         Execute the pending action only after explicit confirmation.
#         """

#         if not confirmed:
#             self.pending_action = None

#             return {
#                 "success": False,
#                 "confirmed": False,
#                 "message": "Appointment booking was cancelled."
#             }

#         if not self.pending_action:
#             return {
#                 "success": False,
#                 "confirmed": False,
#                 "message": "There is no pending action to confirm."
#             }

#         function_name = self.pending_action["function_name"]
#         arguments = self.pending_action["arguments"]

#         execution = self.execute_function_call(
#             function_name,
#             arguments,
#         )

#         if not execution["success"]:
#             return {
#                 "success": False,
#                 "confirmed": True,
#                 "message": execution.get(
#                     "message",
#                     "The appointment could not be booked."
#                 ),
#             }

#         self.pending_action = None

#         return {
#             "success": True,
#             "confirmed": True,
#             "function_name": function_name,
#             "result": execution["result"],
#         }   


import json
from datetime import datetime

from django.core.exceptions import ValidationError
from django.conf import settings
from google import genai

from .tools import (
    get_my_cars,
    get_all_cars,
    get_my_appointments,
    get_maintenance_history,
    get_all_maintenance_records,
    create_maintenance_record,
    get_all_appointments,
    get_all_spare_parts,
    find_available_technicians,
    check_appointment_slot,
    book_appointment,
    find_low_stock_spare_parts,
)


class SmartCarAgent:
    """
    Smart Car Service Agent.

    Main flow:

        User Message
             ↓
        Detect Intent
             ↓
        Collect Required Data
             ↓
        Execute Read-Only Tools
             ↓
        Check Appointment Slot
             ↓
        Ask for Confirmation
             ↓
        Store pending_action
             ↓
        User: Yes / No
             ↓
        Execute book_appointment
             ↓
        Clear pending_action

    Important:
    - The Agent does NOT enforce business permissions.
    - Backend/service layer remains responsible for authorization.
    - IDs are used internally only.
    - IDs are never shown to the user.
    """

    def __init__(self, user):
        self.user = user

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        # Restored from Django session by views.py when available.
        self.pending_action = None

        self.tools = {
            "get_my_cars": get_my_cars,
            "get_all_cars": get_all_cars,
            "get_my_appointments": get_my_appointments,
            "get_maintenance_history": get_maintenance_history,
            "get_all_maintenance_records": get_all_maintenance_records,
            "get_all_appointments": get_all_appointments,
            "get_all_spare_parts": get_all_spare_parts,
            "create_maintenance_record": create_maintenance_record,
            "find_available_technicians": find_available_technicians,
            "check_appointment_slot": check_appointment_slot,
            "book_appointment": book_appointment,
            "find_low_stock_spare_parts": find_low_stock_spare_parts,
        }

    # ============================================================
    # PUBLIC ENTRY POINT
    # ============================================================

    def run_agent_loop(self, user_input):
        

        user_input = user_input.strip()

        if not user_input:
            return {
                "success": False,
                "answer": "Please enter a message.",
            }

        # --------------------------------------------------------
        # 1. Existing pending action
        # --------------------------------------------------------

        if self.pending_action:
            pending_type = self.pending_action.get("type")
            
            if pending_type == "create_maintenance":
                return self._continue_create_maintenance(user_input)
        # New independent request
            intent = self._detect_intent(user_input)

            independent_intents = {
            "my_cars",
            "my_cars_count",
            "car_details",
            "maintenance_history",
            "maintenance_records_check",
            "my_appointments",
            "upcoming_appointments",
            "available_technicians",
            "available_technicians_by_specialization",
            "low_stock",
            "all_cars",
            "all_appointments",
            "all_spare_parts",
            "create_maintenance",
        }

            if intent in independent_intents:
                self.pending_action = None

            else:
                return self._handle_pending_action(user_input)



        intent = self._detect_intent(user_input)

        if intent == "booking":
            return self._handle_booking_request(user_input)
        
        if intent == "create_maintenance":
            return self._handle_create_maintenance_request(user_input)
        
        if intent == "my_cars":
            return self._handle_my_cars()
        
        if intent == "my_cars_count":
            return self._handle_my_cars_count()
        
        if intent == "car_details":
            return self._handle_car_details(user_input)

        if intent == "maintenance_history":
            return self._handle_maintenance_history(user_input)
        
        if intent == "maintenance_records_check":
            return self._handle_maintenance_records_check(user_input)


        if intent == "my_appointments":
            return self._handle_my_appointments()
        
        if intent == "upcoming_appointments":
            return self._handle_upcoming_appointments()

        if intent == "available_technicians":
            return self._handle_available_technicians()
        
        if intent == "available_technicians_by_specialization":
            return self._handle_technicians_by_specialization(user_input)
        if intent == "low_stock":
            return self._handle_low_stock()
        
        if intent == "all_cars":
            return self._handle_all_cars_request()

        if intent == "all_appointments":
            return self._handle_all_appointments_request()
        
        if intent == "all_spare_parts":
            return self._handle_all_spare_parts_request()

        return self._generate_normal_response(user_input)

    

    def _handle_pending_action(self, user_input):
        """
        Handle a message while an action is waiting for confirmation
        or additional booking information.
        """

        # confirmation = self._normalize_confirmation(user_input)

        # # --------------------------------------------------------
        # # Confirmation: YES
        # # --------------------------------------------------------

        # if confirmation == "yes":
        #     return self.confirm_pending_action(True)

        # # --------------------------------------------------------
        # # Confirmation: NO
        # # --------------------------------------------------------

        # if confirmation == "no":
        #     return self.confirm_pending_action(False)

        # # --------------------------------------------------------
        # # Booking is still collecting information
        # # --------------------------------------------------------

        # if self.pending_action.get("status") == "collecting":
        #     return self._continue_booking(user_input)

        # # --------------------------------------------------------
        # # Booking is waiting for confirmation
        # # --------------------------------------------------------

        # if self.pending_action.get("status") == "confirmation":
        #     return {
        #         "success": True,
        #         "tool_used": False,
        #         "confirmation_required": True,
        #         "message": (
        #             "I have a pending appointment booking.\n\n"
        #             "Please reply with Yes to confirm "
        #             "or No to cancel."
        #         ),
        #     }
        pending_type = self.pending_action.get("type")
        pending_status = self.pending_action.get("status")

    # Booking confirmation
        if pending_type == "booking":
            confirmation = self._normalize_confirmation(user_input)

            if confirmation == "yes":
                return self.confirm_pending_action(True)

            if confirmation == "no":
                return self.confirm_pending_action(False)

            if pending_status == "collecting":
                return self._continue_booking(user_input)

            if pending_status == "confirmation":
                return {
                "success": True,
                "tool_used": False,
                "confirmation_required": True,
                "message": (
                    "I have a pending appointment booking.\n\n"
                    "Please reply with Yes to confirm "
                    "or No to cancel."
                ),
            }
        if pending_type == "maintenance_history":
            return self._continue_maintenance_history(user_input)
        if pending_type == "create_maintenance":
            return self._continue_create_maintenance(
            user_input
        )
        self.pending_action = None

        return {
            "success": False,
            "answer": (
                "The previous request could not be continued. "
                "Please start the request again."
            ),
        }

    # ============================================================
    # INTENT DETECTION
    # ============================================================

    def _detect_intent(self, user_input):
        """
        Detect the user's high-level intent.

        This method only decides what the user wants.
        It does not execute tools.
        """

        prompt = f"""
Classify the user's request.

Return ONLY valid JSON.

Format:

{{
    "intent": "unknown"
}}

Allowed intents:

- booking
- my_cars
- my_cars_count
- car_details
- maintenance_history
- maintenance_records_check
- create_maintenance
- my_appointments
- upcoming_appointments
- available_technicians
- available_technicians_by_specialization
- low_stock
- all_cars
- all_appointments
- all_spare_parts
- unknown

Rules:

1. "my cars", "my vehicles", "show me my cars"
   -> my_cars

2. "how many cars do I have"
   -> my_cars_count

3. "all cars", "all vehicles",
   "all cars in the system",
   "every car in the system"
   -> all_cars

4. "my appointments", "my bookings"
   -> my_appointments

5. "upcoming appointments",
   "future appointments"
   -> upcoming_appointments

6. "all appointments",
   "all bookings",
   "all appointments in the system",
   "every appointment"
   -> all_appointments

7. "low stock",
   "low-stock spare parts",
   "spare parts that are low in stock"
   -> low_stock

8. "all spare parts",
   "every spare part",
   "spare parts inventory"
   -> all_spare_parts

9. "maintenance history",
   "what maintenance has my car had",
   "maintenance records"
   -> maintenance_history

10. "which technicians are available"
    -> available_technicians

11. If the user asks for a technician with a
    specific specialization:
    -> available_technicians_by_specialization

12. "book", "make an appointment",
    "schedule a service"
    -> booking

13. NEVER convert "all" into "my".

14. NEVER convert "my" into "all".

15. If the user explicitly asks for system-wide data,
    use the corresponding all_* intent.

16. Return exactly one intent.

User request:
{user_input}
"""

        try:
            response = self.client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt,
            )

            data = json.loads(response.text)

            intent = data.get("intent", "unknown")

            allowed_intents = {
                "booking",
                "my_cars",
                "my_cars_count",
                "car_details",
                "maintenance_history",
                "maintenance_records_check",
                "create_maintenance",
                "my_appointments",
                "upcoming_appointments",
                "available_technicians",
                "available_technicians_by_specialization",
                "low_stock",
                "all_cars",
                "all_appointments",
                "all_spare_parts",
                "unknown",
            }

            if intent not in allowed_intents:
                return "unknown"

            return intent

        except (json.JSONDecodeError, TypeError, AttributeError):
            return "unknown"

    # ============================================================
    # BOOKING
    # ============================================================

    def _handle_booking_request(self, user_input):
        """
        Start or continue a booking conversation.
        """
        if self.user.groups.filter(name="Manager").exists():
            return {
        "success": False,
        "tool_used": False,
        "answer": (
            "Managers are not allowed to book appointments. "
            "Only customers can book appointments."
        ),
    }
        extracted = self._extract_booking_information(user_input)

        if not extracted["success"]:
            return {
                "success": False,
                "answer": extracted.get(
                    "message",
                    "I could not understand the booking details.",
                ),
            }

        booking = extracted["booking"]

        # --------------------------------------------------------
        # Create collecting state
        # --------------------------------------------------------

        self.pending_action = {
            "type": "booking",
            "status": "collecting",
            "arguments": {
                "car_id": booking.get("car_id"),
                "technician_id": booking.get("technician_id"),
                "service_type": booking.get("service_type"),
                "appointment_date": booking.get("appointment_date"),
                "appointment_time": booking.get("appointment_time"),
                "notes": booking.get("notes") or "",
            },
        }

        return self._continue_booking()

    def _continue_booking(self, user_input=None):
        """
        Continue collecting missing booking information.

        The method uses the current pending booking state and,
        when necessary, asks the user for the missing information.
        """

        arguments = self.pending_action["arguments"]

        # --------------------------------------------------------
        # If the user supplied additional information, merge it.
        # --------------------------------------------------------

        if user_input:
            extracted = self._extract_booking_information(user_input)

            if extracted["success"]:
                new_data = extracted["booking"]

                for field in arguments:
                    value = new_data.get(field)

                    if value not in (None, ""):
                        arguments[field] = value

        # --------------------------------------------------------
        # Resolve car using user's cars
        # --------------------------------------------------------

        if not arguments.get("car_id"):

            car_result = self._get_user_cars()

            if not car_result["success"]:
                return {
                    "success": False,
                    "answer": car_result["message"],
                }

            cars = car_result["cars"]

            if not cars:
                self.pending_action = None

                return {
                    "success": False,
                    "answer": "You do not have any cars available for booking.",
                }

            # Try matching a car name from the original conversation.
            selected_car = self._match_car_from_text(
                cars,
                user_input,
            )

            if selected_car:
                arguments["car_id"] = selected_car["id"]

            elif len(cars) == 1:
                # Safe because there is only one car.
                arguments["car_id"] = cars[0]["id"]

            else:
                car_names = [
                    self._format_car_name(car)
                    for car in cars
                ]

                return {
                    "success": True,
                    "tool_used": True,
                    "confirmation_required": False,
                    "message": (
                        "Which car would you like to service?\n\n"
                        + "\n".join(
                            f"- {name}" for name in car_names
                        )
                    ),
                }

        # --------------------------------------------------------
        # Service type
        # --------------------------------------------------------

        if not arguments.get("service_type"):
            return {
                "success": True,
                "confirmation_required": False,
                "message": (
                    "What type of service would you like "
                    "for your car?"
                ),
            }

        # --------------------------------------------------------
        # Technician
        # --------------------------------------------------------

        if not arguments.get("technician_id"):

            technician_result = self._get_available_technicians()

            if not technician_result["success"]:
                return {
                    "success": False,
                    "answer": technician_result["message"],
                }

            technicians = technician_result["technicians"]

            if not technicians:
                return {
                    "success": False,
                    "answer": (
                        "There are currently no available "
                        "technicians."
                    ),
                }

            selected_technician = self._match_technician_from_text(
                technicians,
                user_input,
            )

            if selected_technician:
                arguments["technician_id"] = selected_technician["id"]

            elif len(technicians) == 1:
                arguments["technician_id"] = technicians[0]["id"]

            else:
                names = [
                    technician.get("name", "Unknown technician")
                    for technician in technicians
                ]

                return {
                    "success": True,
                    "tool_used": True,
                    "confirmation_required": False,
                    "message": (
                        "Please choose an available technician:\n\n"
                        + "\n".join(
                            f"- {name}" for name in names
                        )
                    ),
                }

        # --------------------------------------------------------
        # Appointment date
        # --------------------------------------------------------

        if not arguments.get("appointment_date"):
            return {
                "success": True,
                "confirmation_required": False,
                "message": (
                    "What date would you like for the appointment?"
                ),
            }

        # --------------------------------------------------------
        # Appointment time
        # --------------------------------------------------------

        if not arguments.get("appointment_time"):
            return {
                "success": True,
                "confirmation_required": False,
                "message": (
                    "What time would you like for the appointment?"
                ),
            }

        # --------------------------------------------------------
        # Check slot availability
        # --------------------------------------------------------

        slot_result = self._check_appointment_slot(arguments)

        if not slot_result["success"]:
            self.pending_action = None
            return {
                "success": False,
                "tool_used": True,
                "function_name": "check_appointment_slot",
                "error": slot_result["message"],
            }

        tool_result = slot_result["result"]

        if not tool_result.get("available"):
            self.pending_action = None
            return {
                "success": True,
                "tool_used": True,
                "function_name": "check_appointment_slot",
                "confirmation_required": False,
                "answer": (
                    "The appointment slot is not available.\n\n"
                    f"Reason: "
                    f"{tool_result.get('reason', 'Unknown reason.')}"
                ),
            }

        # --------------------------------------------------------
        # Build confirmation state
        # --------------------------------------------------------

        self.pending_action = {
            "type": "booking",
            "status": "confirmation",
            "function_name": "book_appointment",
            "arguments": {
                "car_id": arguments["car_id"],
                "technician_id": arguments["technician_id"],
                "service_type": arguments["service_type"],
                "appointment_date": arguments["appointment_date"],
                "appointment_time": arguments["appointment_time"],
                "notes": arguments.get("notes", ""),
            },
        }

        car = self._find_car_by_id(
            arguments["car_id"]
        )

        technician = tool_result.get("technician", {})

        return {
            "success": True,
            "tool_used": True,
            "function_name": "check_appointment_slot",
            "confirmation_required": True,
            "pending_action": self.pending_action,
            "message": self._build_booking_confirmation_message(
                car=car,
                technician=technician,
                arguments=arguments,
                tool_result=tool_result,
            ),
        }
        
    def _continue_create_maintenance(self, user_input=None):
        """
        Continue collecting information required to create
        a maintenance record.
        """

        arguments = self.pending_action["arguments"]

    
        if user_input:
            extracted = self._extract_maintenance_information(
            user_input
        )

            if extracted["success"]:
                new_data = extracted["maintenance"]

                for field in arguments:
                    value = new_data.get(field)

                    if value not in (None, ""):
                        arguments[field] = value

    
        if not arguments.get("car_id"):

            car_result = self._get_user_cars()

            if not car_result["success"]:
                self.pending_action = None

                return {
                "success": False,
                "answer": car_result["message"],
            }

            cars = car_result["cars"]

            if not cars:
                self.pending_action = None

                return {
                "success": False,
                "answer": (
                    "You do not have any cars available "
                    "for creating a maintenance record."
                ),
            }

            selected_car = self._match_car_from_text(
            cars,
            user_input,
        )

            if selected_car:
                arguments["car_id"] = selected_car["id"]

            elif len(cars) == 1:
                arguments["car_id"] = cars[0]["id"]

            else:
                car_names = [
                self._format_car_name(car)
                for car in cars
            ]

                return {
                "success": True,
                "tool_used": True,
                "confirmation_required": False,
                "message": (
                    "Which car would you like to create "
                    "the maintenance record for?\n\n"
                    + "\n".join(
                        f"- {name}"
                        for name in car_names
                    )
                ),
            }

    

        if not arguments.get("service_type"):
            return {
            "success": True,
            "tool_used": False,
            "confirmation_required": False,
            "message": (
                "What type of maintenance was performed?"
            ),
        }

    

        if not arguments.get("description"):
            return {
            "success": True,
            "tool_used": False,
            "confirmation_required": False,
            "message": (
                "Please provide a short description "
                "of the maintenance."
            ),
        }

    

        if arguments.get("mileage") in (None, ""):
            return {
            "success": True,
            "tool_used": False,
            "confirmation_required": False,
            "message": (
                "What was the car mileage when "
                "the maintenance was performed?"
            ),
        }

    

        if arguments.get("cost") in (None, ""):
            return {
            "success": True,
            "tool_used": False,
            "confirmation_required": False,
            "message": (
                "What was the maintenance cost?"
            ),
        }

   

        if not arguments.get("technician_id"):

            technician_result = (
            self._get_available_technicians()
        )

            if not technician_result["success"]:
                return {
                "success": False,
                "answer": technician_result["message"],
            }

            technicians = technician_result["technicians"]

            if not technicians:
                return {
                "success": False,
                "answer": (
                    "There are currently no available "
                    "technicians."
                ),
            }

            selected_technician = (
            self._match_technician_from_text(
                technicians,
                user_input,
            )
        )

            if selected_technician:
                arguments["technician_id"] = (
                selected_technician["id"]
            )

            elif len(technicians) == 1:
                arguments["technician_id"] = (
                technicians[0]["id"]
            )

            else:
                names = [
                technician.get(
                    "name",
                    "Unknown technician"
                )
                for technician in technicians
            ]

                return {
                "success": True,
                "tool_used": True,
                "confirmation_required": False,
                "message": (
                    "Please choose the technician:\n\n"
                    + "\n".join(
                        f"- {name}"
                        for name in names
                    ))
                }

    

        if not arguments.get("service_date"):
            return {
            "success": True,
            "tool_used": False,
            "confirmation_required": False,
            "message": (
                "What date was the maintenance performed?"
            ),
        }


        if not arguments.get("status"):
            arguments["status"] = "completed"

    

        try:

            result = self.tools[
            "create_maintenance_record"
        ](
            user=self.user,
            car_id=arguments["car_id"],
            technician_id=arguments["technician_id"],
            service_type=arguments["service_type"],
            description=arguments.get(
                "description",
                ""
            ),
            service_date=arguments["service_date"],
            mileage=arguments["mileage"],
            cost=arguments["cost"],
            status=arguments["status"],
        )

            self.pending_action = None

            maintenance = result.get(
            "maintenance_record",
            {}
        )

            return {
            "success": True,
            "tool_used": True,
            "function_name": (
                "create_maintenance_record"
            ),
            "confirmation_required": False,
            "answer": (
                "Maintenance record created successfully.\n\n"
                f"Car: {maintenance.get('car', 'N/A')}\n"
                f"Service: "
                f"{maintenance.get('service_type', 'N/A')}\n"
                f"Technician: "
                f"{maintenance.get('technician', 'N/A')}\n"
                f"Date: "
                f"{maintenance.get('service_date', 'N/A')}\n"
                f"Mileage: "
                f"{maintenance.get('mileage', 'N/A')}\n"
                f"Cost: "
                f"{maintenance.get('cost', 'N/A')}\n"
                f"Status: "
                f"{maintenance.get('status', 'N/A')}"
            ),
            "maintenance_record": maintenance,
        }

        except ValidationError as e:

            self.pending_action = None

            return {
            "success": False,
            "tool_used": True,
            "function_name": (
                "create_maintenance_record"
            ),
            "answer": str(e),
        }

        except Exception as e:

            print(
            f"[Create Maintenance Error] {e}"
        )

            self.pending_action = None

            return {
            "success": False,
            "tool_used": True,
            "function_name": (
                "create_maintenance_record"
            ),
            "answer": (
                "I could not create the "
                "maintenance record."
            ),
        }    

    
    def _extract_booking_information(self, user_input):
        """
        Extract booking information from natural language.

        Missing values are returned as null.
        The model must not invent IDs or missing booking information.
        """
        current_date = datetime.now().strftime("%Y-%m-%d")
        prompt = f"""
Extract appointment booking information from the user's message.
Today's date is: {current_date}
Return ONLY valid JSON.

Structure:

{{
    "car_id": null,
    "technician_id": null,
    "service_type": null,
    "appointment_date": null,
    "appointment_time": null,
    "notes": ""
}}

Rules:

1. Never invent IDs.

2. car_id must be an integer ONLY if the user explicitly
   provides a numeric car ID.

3. technician_id must be an integer ONLY if the user explicitly
   provides a numeric technician ID.

4. Extract service_type when the user explicitly mentions
   a service.

5. Convert explicit natural-language dates to YYYY-MM-DD.

   Examples:
   "29 December" -> use the year based on today's date.
   "December 25" -> use the year based on today's date.
   "25 December" -> use the year based on today's date.

6. If the user provides a date without a year:
   - Use the current year if that date has not passed yet.
   - If the date has already passed in the current year,
     use the next year.

7. appointment_time must be converted to HH:MM.

   Examples:
   "3 PM" -> "15:00"
   "3:00 PM" -> "15:00"
   "10 AM" -> "10:00"
   "10:30 AM" -> "10:30"
   "15:00" -> "15:00"

8. Do NOT treat a time as a date.

9. Do NOT treat a date as a time.

10. If a value is not present in the user's message,
    return null.

11. Do not invent service_type, dates, times, IDs, or notes.

12. Do not add extra fields.


User message:
{user_input}
"""

        try:
            response = self.client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt,
            )

            data = json.loads(response.text)

            return {
                "success": True,
                "booking": {
                    "car_id": data.get("car_id"),
                    "technician_id": data.get("technician_id"),
                    "service_type": data.get("service_type"),
                    "appointment_date": data.get(
                        "appointment_date"
                    ),
                    "appointment_time": data.get(
                        "appointment_time"
                    ),
                    "notes": data.get("notes") or "",
                },
            }

        except (json.JSONDecodeError, TypeError, AttributeError):
            return {
                "success": False,
                "message": (
                    "I could not understand the booking details."
                ),
            }
            
    def _extract_maintenance_information(self, user_input):
        """
        Extract maintenance record information from user input
        using Gemini and return structured JSON data.
        """

        prompt = f"""
Extract maintenance record information from the following user message.

Return ONLY valid JSON.
Do not add markdown.
Do not add explanations.

Allowed fields:

- service_type: string or null
- description: string or null
- service_date: YYYY-MM-DD or null
- mileage: integer or null
- cost: number or null
- status: one of:
  completed
  in_progress
  cancelled
  or null

Rules:

1. If a field is not mentioned, return null.
2. Do not invent missing information.
3. Convert dates to YYYY-MM-DD.
4. Convert mileage to an integer.
5. Convert cost to a number without currency symbols.
6. If the user says the maintenance was completed, use "completed".
7. If the user does not mention status, return null.
8. Keep the description short and meaningful.

Current date: {datetime.now().date()}

User message:
{user_input}
"""

        try:
            response = self.client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

            raw_text = response.text.strip()

            if raw_text.startswith("```"):
                raw_text = raw_text.replace(
                "```json",
                "",
                1,
            ).replace(
                "```",
                "",
                1,
            ).strip()

            data = json.loads(raw_text)

            return {
            "success": True,
            "maintenance": {
                "service_type": data.get(
                    "service_type"
                ),
                "description": data.get(
                    "description"
                ),
                "service_date": data.get(
                    "service_date"
                ),
                "mileage": data.get(
                    "mileage"
                ),
                "cost": data.get(
                    "cost"
                ),
                "status": data.get(
                    "status"
                ),
            },
        }

        except json.JSONDecodeError:
            return {
            "success": False,
            "message": (
                "I could not understand the "
                "maintenance information."
            ),
        }

        except Exception as e:
            print(
            f"[Maintenance Extraction Error] {e}")

            return {
            "success": False,
            "message": (
                "I could not extract the "
                "maintenance information."
            ),
        }        

    # ============================================================
    # TOOL EXECUTION
    # ============================================================

    def _execute_tool(self, function_name, arguments=None):
        """
        Execute an approved backend tool.

        The Agent only controls which registered tool is called.
        Authorization remains inside the service/backend layer.
        """

        tool = self.tools.get(function_name)

        if tool is None:
            return {
                "success": False,
                "message": "Requested function is not available.",
            }

        arguments = arguments or {}

        try:
            result = tool(
                user=self.user,
                **arguments,
            )

            return {
                "success": True,
                "result": result,
            }

        except ValidationError as exc:
            return {
                "success": False,
                "message": str(exc),
            }

        except Exception:
            return {
                "success": False,
                "message": (
                    "The requested operation could not be completed."
                ),
            }

    # ============================================================
    # USER CARS
    # ============================================================

    def _get_user_cars(self):
        """
        Get cars available to the current user.

        The actual authorization/filtering must happen in tools.py
        and the service layer.
        """

        execution = self._execute_tool(
            "get_my_cars"
        )

        if not execution["success"]:
            return {
                "success": False,
                "message": execution["message"],
            }

        result = execution["result"]

        if isinstance(result, dict):
            cars = result.get("cars", [])

        elif isinstance(result, list):
            cars = result

        else:
            cars = []

        return {
            "success": True,
            "cars": cars,
        }

    def _find_car_by_id(self, car_id):
        """
        Find a car from the current user's car list.

        Used only for presentation.
        """

        result = self._get_user_cars()

        if not result["success"]:
            return None

        for car in result["cars"]:
            if str(car.get("id")) == str(car_id):
                return car

        return None

    def _match_car_from_text(self, cars, text):
        """
        Match a car by human-readable information.

        IDs are not shown to the user.
        """

        if not text:
            return None

        text = text.lower()

        for car in cars:
            brand = str(car.get("brand", "")).lower()
            model = str(car.get("model", "")).lower()

            if brand and brand in text and model and model in text:
                return car

        for car in cars:
            brand = str(car.get("brand", "")).lower()
            model = str(car.get("model", "")).lower()

            if brand and brand in text:
                return car

            if model and model in text:
                return car

        return None

    def _format_car_name(self, car):
        brand = car.get("brand", "")
        model = car.get("model", "")

        name = f"{brand} {model}".strip()

        if name:
            return name

        return "Your car"
    
    def _handle_my_cars(self):
        """
        Show cars belonging to the current user.

        IDs are used internally only and are never shown
        to the user.
        """

        result = self._get_user_cars()

        if not result["success"]:
            return {
            "success": False,
            "answer": result["message"],
        }

        cars = result["cars"]

        if not cars:
            return {
            "success": True,
            "tool_used": True,
            "function_name": "get_my_cars",
            "answer": "You do not have any registered cars.",
        }

        lines = []

        for car in cars:
            name = self._format_car_name(car)

            details = []

            if car.get("year"):
                details.append(str(car["year"]))

            if car.get("license_plate"):
                details.append(
                f"Plate: {car['license_plate']}"
            )

            if car.get("color"):
                details.append(
                f"Color: {car['color']}"
            )

            if details:
                lines.append(
                f"- {name} ({', '.join(details)})"
            )
            else:
                lines.append(
                f"- {name}"
            )

        return {
        "success": True,
        "tool_used": True,
        "function_name": "get_my_cars",
        "tool_result": result,
        "answer": (
            "Your cars:\n\n"
            + "\n".join(lines)
        ),
    }
        
    def _handle_my_cars_count(self):
        """
        Return the number of cars belonging to the current user.
        """

        result = self._get_user_cars()

        if not result["success"]:
            return {
            "success": False,
            "answer": result["message"],
        }

        cars = result["cars"]
        count = len(cars)

        if count == 0:
            message = "You do not have any registered cars."

        elif count == 1:
            message = "You have 1 car."

        else:
            message = f"You have {count} cars."

        return {
        "success": True,
        "tool_used": True,
        "function_name": "get_my_cars",
        "answer": message,
    }    
    # ============================================================
    # TECHNICIANS
    # ============================================================

    def _get_available_technicians(self):
        """
        Get available technicians through the backend tool.
        """

        execution = self._execute_tool(
            "find_available_technicians"
        )

        if not execution["success"]:
            return {
                "success": False,
                "message": execution["message"],
            }

        result = execution["result"]

        if isinstance(result, dict):
            technicians = result.get(
                "technicians",
                []
            )

        elif isinstance(result, list):
            technicians = result

        else:
            technicians = []

        return {
            "success": True,
            "technicians": technicians,
        }

    def _match_technician_from_text(
        self,
        technicians,
        text,
    ):
        """
        Match a technician by name.
        """

        if not text:
            return None

        text = text.lower()

        for technician in technicians:
            name = str(
                technician.get("name", "")
            ).lower()

            if name and name in text:
                return technician

        return None

    # ============================================================
    # APPOINTMENT SLOT
    # ============================================================

    def _check_appointment_slot(self, arguments):
        """
        Check whether the requested appointment slot is available.
        """

        execution = self._execute_tool(
            "check_appointment_slot",
            {
                "technician_id": arguments["technician_id"],
                "appointment_date": arguments[
                    "appointment_date"
                ],
                "appointment_time": arguments[
                    "appointment_time"
                ],
            },
        )

        return execution

    # ============================================================
    # CONFIRMATION
    # ============================================================

    def confirm_pending_action(self, confirmed):
        """
        Execute or cancel a pending appointment booking.
        """

        if not self.pending_action:
            return {
                "success": False,
                "confirmed": False,
                "message": (
                    "There is no pending action to confirm."
                ),
            }

        if not confirmed:
            self.pending_action = None

            return {
                "success": True,
                "confirmed": False,
                "message": (
                    "Appointment booking was cancelled."
                ),
            }

        if self.pending_action.get("status") != "confirmation":
            return {
                "success": False,
                "confirmed": False,
                "message": (
                    "The appointment is not ready "
                    "for confirmation."
                ),
            }

        function_name = self.pending_action.get(
            "function_name"
        )

        arguments = self.pending_action.get(
            "arguments",
            {}
        )

        execution = self._execute_tool(
            function_name,
            arguments,
        )

        if not execution["success"]:
            return {
                "success": False,
                "confirmed": True,
                "message": execution.get(
                    "message",
                    "The appointment could not be booked.",
                ),
            }

        result = execution["result"]

        # IMPORTANT:
        # Clear the pending action only after successful booking.
        self.pending_action = None

        return {
            "success": True,
            "confirmed": True,
            "function_name": function_name,
            "result": result,
        }

    # ============================================================
    # MAINTENANCE HISTORY
    # ============================================================

    def _handle_maintenance_history(self, user_input):
        """
        Handle maintenance-history requests.

        If the user has one car, use it automatically.
        Otherwise ask the user which car they mean.
        """

        car_result = self._get_user_cars()

        if not car_result["success"]:
            return {
                "success": False,
                "answer": car_result["message"],
            }

        cars = car_result["cars"]

        if not cars:
            return {
                "success": False,
                "answer": (
                    "You do not have any cars "
                    "with maintenance history."
                ),
            }

        selected_car = self._match_car_from_text(
            cars,
            user_input,
        )

        if selected_car is None and len(cars) == 1:
            selected_car = cars[0]

        # if selected_car is None:
        #     return {
        #         "success": True,
        #         "tool_used": True,
        #         "message": (
        #             "Which car would you like to see "
        #             "the maintenance history for?\n\n"
        #             + "\n".join(
        #                 f"- {self._format_car_name(car)}"
        #                 for car in cars
        #             )
        #         ),
        #     }
        
        if selected_car is None:
            self.pending_action = {
        "type": "maintenance_history",
        "status": "collecting",
        "cars": cars,
    }

            return {
        "success": True,
        "tool_used": True,
        "confirmation_required": False,
        "message": (
            "Which car would you like to see "
            "the maintenance history for?\n\n"
            + "\n".join(
                f"- {self._format_car_name(car)}"
                for car in cars
            )
        ),
    }

        execution = self._execute_tool(
            "get_maintenance_history",
            {
                "car_id": selected_car["id"]
            },
        )

        if not execution["success"]:
            return {
                "success": False,
                "tool_used": True,
                "error": execution["message"],
            }

        return {
            "success": True,
            "tool_used": True,
            "function_name": "get_maintenance_history",
            "tool_result": execution["result"],
            "answer": self._format_maintenance_result(
                selected_car,
                execution["result"],
            ),
        }

    # ============================================================
    # MY APPOINTMENTS
    # ============================================================

    def _handle_my_appointments(self):
        """
        Show appointments belonging to the current user.
        """

        execution = self._execute_tool(
            "get_my_appointments"
        )

        if not execution["success"]:
            return {
                "success": False,
                "answer": execution["message"],
            }

        result = execution["result"]

        appointments = (
            result.get("appointments", [])
            if isinstance(result, dict)
            else result
        )

        if not appointments:
            return {
                "success": True,
                "tool_used": True,
                "answer": (
                    "You currently have no appointments."
                ),
            }

        lines = []

        for appointment in appointments:
            car = appointment.get("car", "Your car")
            technician = appointment.get(
                "technician",
                "Assigned technician",
            )
            service = appointment.get(
                "service_type",
                "Service",
            )
            appointment_date = appointment.get(
                "appointment_date",
                "",
            )
            appointment_time = appointment.get(
                "appointment_time",
                "",
            )
            status = appointment.get(
                "status",
                "",
            )

            lines.append(
                f"- {car} | "
                f"{service} | "
                f"{appointment_date} "
                f"{appointment_time} | "
                f"{technician} | "
                f"{status}"
            )

        return {
            "success": True,
            "tool_used": True,
            "function_name": "get_my_appointments",
            "tool_result": result,
            "answer": (
                "Your appointments:\n\n"
                + "\n".join(lines)
            ),
        }

    # ============================================================
    # AVAILABLE TECHNICIANS
    # ============================================================

    def _handle_available_technicians(self):
        """
        Show currently available technicians.
        """

        result = self._get_available_technicians()

        if not result["success"]:
            return {
                "success": False,
                "answer": result["message"],
            }

        technicians = result["technicians"]

        if not technicians:
            return {
                "success": True,
                "tool_used": True,
                "answer": (
                    "There are currently no available technicians."
                ),
            }

        lines = []

        for technician in technicians:
            name = technician.get(
                "name",
                "Unknown technician",
            )

            specialization = technician.get(
                "specialization",
                "",
            )

            if specialization:
                lines.append(
                    f"- {name} — {specialization}"
                )
            else:
                lines.append(
                    f"- {name}"
                )

        return {
            "success": True,
            "tool_used": True,
            "function_name": "find_available_technicians",
            "tool_result": technicians,
            "answer": (
                "Available technicians:\n\n"
                + "\n".join(lines)
            ),
        }

    # ============================================================
    # LOW STOCK
    # ============================================================

    def _handle_low_stock(self):

        # if not self._is_staff_user():
        
        # allowed_groups = ["Admin", "Manager"] 
        # if not self.user.groups.filter( name__in=allowed_groups ).exists():
        #     print("LOW STOCK ACCESS CHECK")
        #     print("USER:", self.user.username)
        #     print("GROUPS:", list(self.user.groups.values_list("name", flat=True)))
        print("=== LOW STOCK ===")
        print("USER:", self.user.username)
        print(
        "GROUPS:",
        list(self.user.groups.values_list("name", flat=True))
    )

        allowed = self.user.groups.filter(
        name__in=["Admin", "Manager"]
    ).exists()

        print("ALLOWED:", allowed)

        if not allowed:
            print(">>> CUSTOMER BLOCKED <<<")
            return {
            "success": False,
            "tool_used": False,
            "answer": (
                "You do not have permission to access "
                "low-stock spare parts."
            ),
        }

        try:
            result = self.tools["find_low_stock_spare_parts"](
            self.user
        )

            parts = result.get("spare_parts", [])

            if not parts:
                return {
                "success": True,
                "tool_used": True,
                "function_name": "find_low_stock_spare_parts",
                "answer": (
                    "There are currently no low-stock "
                    "spare parts."
                ),
            }

            lines = ["Low-stock spare parts:", ""]

            for part in parts:
                lines.append(
                f"- {part['name']} | "
                f"Part Number: {part['part_number']} | "
                f"Quantity: {part['quantity']} | "
                f"Minimum: {part['minimum_stock']}"
            )

            return {
            "success": True,
            "tool_used": True,
            "function_name": "find_low_stock_spare_parts",
            "answer": "\n".join(lines),
        }

        except ValidationError as e:
            return {
            "success": False,
            "tool_used": True,
            "function_name": "find_low_stock_spare_parts",
            "answer": str(e),
        }

        except Exception:
            return {
            "success": False,
            "tool_used": True,
            "function_name": "find_low_stock_spare_parts",
            "answer": (
                "I could not retrieve the spare parts inventory."
            ),
        }


    def _generate_normal_response(self, user_input):
        """
        Generate a normal conversational response when
        no backend tool is required.
        """

        prompt = f"""
You are a friendly Smart Car Service Assistant.

Answer the user's message clearly and simply.

You can help with:
- booking service appointments
- maintenance history
- available technicians
- user's appointments
- other Smart Car Service questions

Do not invent database information.
Do not mention internal tools, IDs, database implementation,
ORM, or backend implementation.

User:
{user_input}
"""

        try:
            response = self.client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt,
            )

            return {
                "success": True,
                "tool_used": False,
                "answer": response.text,
            }

        except Exception:
            return {
                "success": False,
                "answer": (
                    "Sorry, I could not process your request."
                ),
            }

    # ============================================================
    # RESPONSE FORMATTERS
    # ============================================================

    def _build_booking_confirmation_message(
        self,
        car,
        technician,
        arguments,
        tool_result,
    ):
        """
        Build the confirmation message shown to the user.

        Internal IDs are intentionally excluded.
        """

        car_name = (
            self._format_car_name(car)
            if car
            else "Your car"
        )

        technician_name = technician.get(
            "name",
            "Assigned technician",
        )

        specialization = technician.get(
            "specialization",
            "",
        )

        message = (
            "The appointment slot is available.\n\n"
            f"Car: {car_name}\n"
            f"Technician: {technician_name}\n"
        )

        if specialization:
            message += (
                f"Specialization: {specialization}\n"
            )

        message += (
            f"Service: {arguments['service_type']}\n"
            f"Date: {arguments['appointment_date']}\n"
            f"Time: {arguments['appointment_time']}\n"
        )

        if arguments.get("notes"):
            message += (
                f"Notes: {arguments['notes']}\n"
            )

        message += (
            "\nDo you confirm this appointment?"
        )

        return message

    # def _format_maintenance_result(
    #     self,
    #     car,
    #     result,
    # ):
    #     """
    #     Format maintenance history without exposing IDs.
    #     """

    #     car_name = self._format_car_name(car)

    #     history = (
    #         result.get("history", [])
    #         if isinstance(result, dict)
    #         else result
    #     )

    #     if not history:
    #         return (
    #             f"No maintenance history was found "
    #             f"for {car_name}."
    #         )

    #     lines = []

    #     for item in history:
    #         service = item.get(
    #             "service_type",
    #             "Maintenance service",
    #         )

    #         service_date = item.get(
    #             "date",
    #             item.get(
    #                 "service_date",
    #                 "",
    #             ),
    #         )

    #         notes = item.get(
    #             "notes",
    #             "",
    #         )

    #         line = f"- {service}"

    #         if service_date:
    #             line += f" — {service_date}"

    #         if notes:
    #             line += f" — {notes}"

    #         lines.append(line)

    #     return (
    #         f"Maintenance history for {car_name}:\n\n"
    #         + "\n".join(lines)
    #     )
    def _format_maintenance_result(self, car, result):
        car_name = self._format_car_name(car)

        if isinstance(result, dict):
            history = result.get(
            "maintenance_history",
            result.get("history", [])
        )
        else:
            history = result

        if not history:
            return (
            f"No maintenance history was found "
            f"for {car_name}."
        )

        lines = []

        for item in history:
            service = item.get(
            "service_type",
            "Maintenance service",
        )

            service_date = item.get(
            "service_date",
            item.get("date", ""),
        )

            mileage = item.get("mileage")
            cost = item.get("cost")
            status = item.get("status")
            technician = item.get("technician")

            line = f"- {service}"

            if service_date:
                line += f" — {service_date}"

            if mileage is not None:
                line += f" — Mileage: {mileage}"

            if cost is not None:
                line += f" — Cost: {cost}"

            if status:
                line += f" — Status: {status}"

            if technician:
                line += f" — Technician: {technician}"

            lines.append(line)

        return (
        f"Maintenance history for {car_name}:\n\n"
        + "\n".join(lines)
    )

    def _format_low_stock_result(self, result):
        """
        Format low-stock spare parts without exposing IDs.
        """

        parts = (
            result.get("parts", [])
            if isinstance(result, dict)
            else result
        )

        if not parts:
            return "No low-stock spare parts were found."

        lines = []

        for part in parts:
            name = part.get(
                "name",
                "Unknown spare part",
            )

            quantity = part.get(
                "quantity",
                part.get(
                    "stock_quantity",
                    "",
                ),
            )

            minimum = part.get(
                "minimum_stock",
                "",
            )

            if quantity != "" and minimum != "":
                lines.append(
                    f"- {name}: "
                    f"{quantity} available "
                    f"(minimum {minimum})"
                )
            elif quantity != "":
                lines.append(
                    f"- {name}: "
                    f"{quantity} available"
                )
            else:
                lines.append(
                    f"- {name}"
                )

        return (
            "Low-stock spare parts:\n\n"
            + "\n".join(lines)
        )

    # ============================================================
    # CONFIRMATION NORMALIZATION
    # ============================================================

    @staticmethod
    def _normalize_confirmation(user_input):
        """
        Convert different confirmation messages into:
        yes / no / None
        """

        value = user_input.strip().lower()

        yes_values = {
            "yes",
            "y",
            "confirm",
            "confirmed",
            "approve",
            "approved",
            "ok",
            "okay",
            "sure",
            "go ahead",
        }

        no_values = {
            "no",
            "n",
            "cancel",
            "cancelled",
            "canceled",
            "decline",
            "declined",
            "reject",
            "rejected",
        }

        if value in yes_values:
            return "yes"

        if value in no_values:
            return "no"

        return None
    
    def _continue_maintenance_history(self, user_input):
        """
        Continue maintenance history flow after asking
        the user to select a car.
        """

        cars = self.pending_action.get("cars", [])

        if not cars:
            self.pending_action = None

            return {
            "success": False,
            "answer": (
                "I could not find your cars. "
                "Please start the request again."
            ),
        }

        selected_car = self._match_car_from_text(
        cars,
        user_input,
    )

        if selected_car is None:
            return {
            "success": True,
            "tool_used": False,
            "confirmation_required": False,
            "message": (
                "I could not identify that car.\n\n"
                "Please choose one of these cars:\n\n"
                + "\n".join(
                    f"- {self._format_car_name(car)}"
                    for car in cars
                )
            ),
        }

    # Clear pending state before executing the tool
        self.pending_action = None

        execution = self._execute_tool(
        "get_maintenance_history",
        {
            "car_id": selected_car["id"],
        },
    )

        if not execution["success"]:
            return {
            "success": False,
            "tool_used": True,
            "function_name": "get_maintenance_history",
            "error": execution["message"],
        }

        return {
        "success": True,
        "tool_used": True,
        "function_name": "get_maintenance_history",
        "tool_result": execution["result"],
        "answer": self._format_maintenance_result(
            selected_car,
            execution["result"],
        ),
    }
        
    def _handle_technicians_by_specialization(self, user_input):
        result = self._get_available_technicians()

        if not result["success"]:
            return {
            "success": False,
            "answer": result["message"],
        }

        technicians = result["technicians"]

        if not technicians:
            return {
            "success": True,
            "tool_used": True,
            "answer": (
                "There are currently no available technicians."
            ),
        }

        text = user_input.lower()

        matching_technicians = []

        for technician in technicians:
            specialization = str(
            technician.get("specialization", "")
        ).lower()

            if specialization and specialization in text:
                matching_technicians.append(technician)

        if not matching_technicians:
            return {
            "success": True,
            "tool_used": True,
            "function_name": "find_available_technicians",
            "answer": (
                "I could not find an available technician "
                "with that specialization."
            ),
        }

        lines = []

        for technician in matching_technicians:
            name = technician.get(
            "name",
            "Unknown technician",
        )
            specialization = technician.get(
            "specialization",
            "",
        )

            lines.append(
            f"- {name} — {specialization}"
        )

        return {
        "success": True,
        "tool_used": True,
        "function_name": "find_available_technicians",
        "answer": (
            "Yes. I found an available technician "
            "with that specialization:\n\n"
            + "\n".join(lines)
        ),
    }    
        
    def _handle_upcoming_appointments(self):
        result = self._execute_tool("get_my_appointments")

        if not result["success"]:
            return {
            "success": False,
            "answer": result["message"],
        }

        data = result["result"]

        if isinstance(data, dict):
            appointments = data.get("appointments", [])
        elif isinstance(data, list):
            appointments = data
        else:
            appointments = []

        now = datetime.now()

        upcoming = []

        for appointment in appointments:
            appointment_date = appointment.get("appointment_date")
            appointment_time = appointment.get("appointment_time")

            if not appointment_date or not appointment_time:
                continue

            try:
                appointment_datetime = datetime.strptime(
                f"{appointment_date} {appointment_time}",
                "%Y-%m-%d %H:%M:%S",
            )
            except ValueError:
                try:
                    appointment_datetime = datetime.strptime(
                    f"{appointment_date} {appointment_time}",
                    "%Y-%m-%d %H:%M",
                )
                except ValueError:
                    continue

            if appointment_datetime <= now:
                continue

            status = str(
            appointment.get("status", "")
        ).lower()

            if status in {"completed", "cancelled", "canceled"}:
                continue

            upcoming.append(
            (
                appointment_datetime,
                appointment,
            )
        )

        upcoming.sort(key=lambda item: item[0])

        if not upcoming:
            return {
            "success": True,
            "tool_used": True,
            "function_name": "get_my_appointments",
            "answer": "You do not have any upcoming appointments.",
        }

        lines = []

        for appointment_datetime, appointment in upcoming:
            car = appointment.get("car", "Unknown car")
            service = appointment.get(
            "service_type",
            "Service",
        )
            technician = appointment.get(
            "technician",
            "Unknown technician",
        )
            status = appointment.get(
            "status",
            "unknown",
        )

            lines.append(
            f"- {car} | {service} | "
            f"{appointment_datetime.strftime('%Y-%m-%d %H:%M')} | "
            f"{technician} | {status}"
        )

        count = len(upcoming)

        if count == 1:
            intro = "Yes, you have 1 upcoming appointment:"
        else:
            intro = (
            f"Yes, you have {count} upcoming appointments:"
        )

        return {
        "success": True,
        "tool_used": True,
        "function_name": "get_my_appointments",
        "tool_result": {
            "appointments": [
                appointment
                for _, appointment in upcoming
            ]
        },
        "answer": (
            intro
            + "\n\n"
            + "\n".join(lines)
        ),
    } 
    
    def _normalize_date(self, date_text):
        """
        Convert natural language date into YYYY-MM-DD.

        Examples:
        29 December -> 2026-12-29
        December 25 -> 2026-12-25
        """

        if not date_text:
            return None

        date_text = date_text.strip()

        try:
            from dateutil import parser
            from django.utils import timezone

            now = timezone.localtime()

            parsed = parser.parse(
            date_text,
            default=now.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            ),
        )

        # If user did not specify a year,
        # dateutil may use current year.
        # If that date has already passed,
        # use next year.
            if not any(
                char.isdigit() for char in date_text
        ):
                pass

            result = parsed.date()

        # Handle dates without explicit year
            if result < now.date() and (
            now.strftime("%B").lower() not in date_text.lower()
            or str(now.year) not in date_text
        ):
                result = result.replace(
                year=result.year + 1
            )

            return result.isoformat()

        except (ValueError, OverflowError):
            return None   
        
    def _normalize_time(self, time_text):
        """
        Convert natural language time into HH:MM.

        Examples:
        3 PM -> 15:00
        10:30 AM -> 10:30
        7:57 PM -> 19:57
        """

        if not time_text:
            return None

        time_text = time_text.strip()

        try:
            from dateutil import parser

            parsed = parser.parse(time_text)

            return parsed.strftime("%H:%M")

        except (ValueError, OverflowError):
            return None    
        
    def _is_staff_user(self):
        return self.user.groups.filter(
        name__in=["Admin", "Manager"]).exists()   
        
    def _handle_all_cars_request(self):

        if not self._is_staff_user():
            return {
            "success": False,
            "tool_used": False,
            "answer": (
                "You do not have permission to view "
                "all cars in the system."
            ),
        }
            
        try:
            result = self.tools["get_all_cars"](
            user=self.user
        )

            cars = result.get("cars", [])

            if not cars:
                return {
                "success": True,
                "tool_used": True,
                "function_name": "get_all_cars",
                "answer": "There are currently no customer cars.",
            }

            lines = ["All customer cars:", ""]

            for car in cars:
                lines.append(
                f"- {car['brand']} {car['model']} "
                f"({car['year']}) | "
                f"License Plate: {car['license_plate']} | "
                f"Owner: {car['owner']} | "
                f"Mileage: {car['mileage']} | "
                f"Color: {car['color'] or 'N/A'}"
            )

            return {
            "success": True,
            "tool_used": True,
            "function_name": "get_all_cars",
            "answer": "\n".join(lines),
            "cars": cars,
        }

        except ValidationError as e:
            return {
            "success": False,
            "tool_used": True,
            "function_name": "get_all_cars",
            "answer": str(e),
        }

        except Exception as e:
            print(f"[All Cars Error] {e}")

            return {
            "success": False,
            "tool_used": True,
            "function_name": "get_all_cars",
            "answer": "I could not retrieve the customer cars.",
        }    

    def _handle_all_appointments_request(self):

        if not self._is_staff_user():
            return {
            "success": False,
            "tool_used": False,
            "answer": (
                "You do not have permission to view "
                "all appointments in the system."
            ),
        }
            
        try:
            result = self.tools["get_all_appointments"](
            user=self.user
        )

            appointments = result.get("appointments", [])

            if not appointments:
                return {
                "success": True,
                "tool_used": True,
                "function_name": "get_all_appointments",
                "answer": (
                    "There are currently no customer appointments."
                ),
            }

            lines = [
            "All customer appointments:",
            ""
        ]

            for appointment in appointments:
                lines.append(
                f"- Customer: {appointment['customer']} | "
                f"Car: {appointment['car']} | "
                f"Service: {appointment['service_type']} | "
                f"Technician: {appointment['technician']} | "
                f"Date: {appointment['appointment_date']} | "
                f"Time: {appointment['appointment_time']} | "
                f"Status: {appointment['status']}"
            )

            return {
            "success": True,
            "tool_used": True,
            "function_name": "get_all_appointments",
            "answer": "\n".join(lines),
            "appointments": appointments,
        }

        except ValidationError as e:
            return {
            "success": False,
            "tool_used": True,
            "function_name": "get_all_appointments",
            "answer": str(e),
        }

        except Exception as e:
            print(f"[All Appointments Error] {e}")

            return {
            "success": False,
            "tool_used": True,
            "function_name": "get_all_appointments",
            "answer": (
                "I could not retrieve the customer appointments."
            ),
        }    

    def _handle_all_spare_parts_request(self):

        if not self._is_staff_user():
            return {
            "success": False,
            "tool_used": False,
            "answer": (
                "You do not have permission to view "
                "spare parts inventory."
            ),
        }
            
        try:
            result = self.tools["get_all_spare_parts"](
            user=self.user
        )

            parts = result.get("spare_parts", [])

            if not parts:
                return {
                "success": True,
                "tool_used": True,
                "function_name": "get_all_spare_parts",
                "answer": (
                    "There are currently no spare parts "
                    "in the inventory."
                ),
            }

            lines = [
            "All spare parts:",
            ""
        ]

            for part in parts:
                lines.append(
                f"- {part['name']} | "
                f"Part Number: {part['part_number']} | "
                f"Quantity: {part['quantity']} | "
                f"Minimum Stock: {part['minimum_stock']} | "
                f"Price: {part['price']}"
            )

            return {
            "success": True,
            "tool_used": True,
            "function_name": "get_all_spare_parts",
            "answer": "\n".join(lines),
            "spare_parts": parts,
        }

        except ValidationError as e:
            return {
            "success": False,
            "tool_used": True,
            "function_name": "get_all_spare_parts",
            "answer": str(e),
        }

        except Exception as e:
            print(f"[All Spare Parts Error] {e}")

            return {
            "success": False,
            "tool_used": True,
            "function_name": "get_all_spare_parts",
            "answer": (
                "I could not retrieve the spare parts inventory."
            ),
        }    
            
    def _select_car_from_input(self, user_input):

        result = self._get_user_cars()

        if not result["success"]:
            return None

        cars = result["cars"]

        normalized_input = user_input.strip().lower()

        matches = []

        for car in cars:

            car_name = (
            f"{car['brand']} {car['model']}"
        ).lower()

            if car_name == normalized_input:
                matches.append(car)

        if len(matches) == 1:
            return matches[0]

        return None        
    
    def _select_technician_from_input(
    self,
    user_input,
    technicians,
):

        normalized_input = user_input.strip().lower()

        for technician in technicians:

            name = technician.get(
            "name",
            ""
        ).strip().lower()

            specialization = technician.get(
            "specialization",
            ""
        ).strip().lower()

            if normalized_input == name:
                return technician

            if normalized_input == specialization:
                return technician

        return None
    
    def _handle_maintenance_records_check(self, user_input):

        if not self._is_staff_user():
            return {
            "success": False,
            "tool_used": False,
            "answer": (
                "You do not have permission to view "
                "all maintenance records."
            ),
        }

        try:
            result = self.tools["get_all_maintenance_records"](
            user=self.user
        )

            records = result.get("maintenance_records", [])

            if not records:
                return {
                "success": True,
                "tool_used": True,
                "function_name": "get_all_maintenance_records",
                "answer": (
                    "There are currently no customer "
                    "maintenance records."
                ),
            }

            lines = ["All customer maintenance records:", ""]

            for record in records:
                lines.append(
                f"- Customer: {record['customer']} | "
                f"Car: {record['car']} | "
                f"Service: {record['service_type']} | "
                f"Technician: {record['technician']} | "
                f"Date: {record['service_date']} | "
                f"Cost: {record['cost']} | "
                f"Status: {record['status']}"
            )

            return {
            "success": True,
            "tool_used": True,
            "function_name": "get_all_maintenance_records",
            "answer": "\n".join(lines),
            "maintenance_records": records,
        }

        except ValidationError as e:
            return {
            "success": False,
            "tool_used": True,
            "function_name": "get_all_maintenance_records",
            "answer": str(e),
        }

        except Exception as e:
            print(f"[All Maintenance Error] {e}")

            return {
            "success": False,
            "tool_used": True,
            "function_name": "get_all_maintenance_records",
            "answer": (
                "I could not retrieve the customer "
                "maintenance records."
            ),
        }
            
    def _handle_create_maintenance_request(self, user_input):

        if self.user.groups.filter(name="Manager").exists():
            return {
            "success": False,
            "tool_used": False,
            "answer": (
                "Managers cannot create maintenance records. "
                "Only customers can create maintenance records."
            ),
        }

        if self.user.groups.filter(name="Manager").exists():
            return {
        "success": False,
        "tool_used": False,
        "answer": (
            "Managers cannot create maintenance records. "
            "Only customers can create maintenance records."
        ),
    }
        if self.user.groups.filter(name="Admin").exists():
           return {
        "success": False,
        "tool_used": False,
        "answer": (
            "Admins cannot create maintenance records. "
            "Only customers can create maintenance records."
        ),
    }

        try:
            cars_result = self.tools["get_my_cars"](
            self.user
        )

            cars = cars_result or []

            if isinstance(cars_result, dict):
                cars = cars_result.get("cars", [])

            if not cars:
                return {
                "success": False,
                "tool_used": True,
                "function_name": "get_my_cars",
                "answer": (
                    "You do not have any cars available "
                    "for creating a maintenance record."
                ),
            }

            if len(cars) == 1:
                car = cars[0]

                self.pending_action = {
        "type": "create_maintenance",
        "status": "collecting",
        "arguments": {
            "car_id": car["id"],
            "technician_id": None,
            "service_type": None,
            "description": "",
            "service_date": None,
            "mileage": None,
            "cost": None,
            "status": "completed",
        },
    }

                return {
                "success": True,
                "tool_used": True,
                "function_name": "get_my_cars",
                "answer": (
                    f"Selected car: "
                    f"{car['brand']} {car['model']}\n\n"
                    "What type of maintenance was performed?"
                ),
            }

        
            lines = [
            "Which car would you like to create "
            "the maintenance record for?",
            ""
        ]

            for index, car in enumerate(cars, start=1):
                lines.append(
                f"{index}. "
                f"{car['brand']} {car['model']} "
                f"({car['year']})"
            )

            self.pending_action = {
            "type": "create_maintenance",
            "step": "car",
            "cars": cars,
        }

            return {
            "success": True,
            "tool_used": True,
            "function_name": "get_my_cars",
            "answer": "\n".join(lines),
        }

        except ValidationError as e:
            return {
            "success": False,
            "tool_used": True,
            "function_name": "get_my_cars",
            "answer": str(e),
        }

        except Exception as e:
            print(
            f"[Create Maintenance Request Error] {e}"
        )

            return {
            "success": False,
            "tool_used": True,
            "function_name": "get_my_cars",
            "answer": (
                "I could not start the maintenance "
                "record process."
            ),
        }        

