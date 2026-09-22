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

import json
from django.core.exceptions import ValidationError
from google import genai
from google.genai import types
from django.conf import settings
from datetime import date, time, datetime
from .tools import (
    get_maintenance_history,
    find_available_technicians,
    check_appointment_slot,
    book_appointment,
    find_low_stock_spare_parts)
from cars.models import Car


class SmartCarAgent:
    """
    Smart Car Agent.

    Flow:
    User Input
        ↓
    LLM Reasoning
        ↓
    Tool Selection
        ↓
    Parameter Validation
        ↓
    Tool Execution
        ↓
    Observation
        ↓
    Final Response
    """

    def __init__(self, user):
        self.user = user

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )
        
        self.pending_action = None

        self.tools = {
            "get_maintenance_history": get_maintenance_history,
            "find_available_technicians": find_available_technicians,
            "check_appointment_slot": check_appointment_slot,
            "book_appointment": book_appointment,
            "find_low_stock_spare_parts": find_low_stock_spare_parts,
        }
        
        self.function_declarations = [
            types.FunctionDeclaration(
        name="get_maintenance_history",
        description="Get the maintenance history of a specific car.",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "car_id": types.Schema(
                    type="INTEGER",
                    description="The ID of the car."
                )
            },
            required=["car_id"],
        ),
    ),

            types.FunctionDeclaration(
        name="find_available_technicians",
        description="Find technicians who are currently available.",
        parameters=types.Schema(
            type="OBJECT",
            properties={},
        ),
    ),

            types.FunctionDeclaration(
    name="check_appointment_slot",
    description="Check whether a technician appointment slot is available.",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "technician_id": types.Schema(
                type="INTEGER",
                description="The technician ID."
            ),
            "appointment_date": types.Schema(
                type="STRING",
                description="Appointment date in YYYY-MM-DD format."
            ),
            "appointment_time": types.Schema(
                type="STRING",
                description="Appointment time in HH:MM format."
            ),
        },
        required=[
            "technician_id",
            "appointment_date",
            "appointment_time",
        ],
    ),
),

            types.FunctionDeclaration(
        name="book_appointment",
        description="Book a service appointment for a user's car.",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "car_id": types.Schema(
                    type="INTEGER",
                    description="The user's car ID."
                ),
                "technician_id": types.Schema(
                    type="INTEGER",
                    description="The technician ID."
                ),
                "service_type": types.Schema(
                    type="STRING",
                    description="Type of service requested."
                ),
                "appointment_date": types.Schema(
                    type="STRING",
                    description="Appointment date in YYYY-MM-DD format."
                ),
                "appointment_time": types.Schema(
                    type="STRING",
                    description="Appointment time in HH:MM format."
                ),
                "notes": types.Schema(
                    type="STRING",
                    description="Optional appointment notes."
                ),
            },
            required=[
                "car_id",
                "technician_id",
                "service_type",
                "appointment_date",
                "appointment_time",
            ],
        ),
    ),
            types.FunctionDeclaration(
    name="find_low_stock_spare_parts",
    description="Find spare parts whose stock quantity is at or below the minimum stock level.",
    parameters=types.Schema(
        type="OBJECT",
        properties={},
    ),
),
]

    def perceive_goal(self, user_input):
        """
        Ask the LLM to understand the user's goal.
        """

        prompt = f"""
You are the reasoning component of a Smart Car Service system.

Analyze the user's request and return ONLY valid JSON.

Available goals:

1. maintenance_history
2. available_technicians
3. appointment
4. unknown

User request:
{user_input}

Return exactly:

{{
    "goal": "one of the available goals",
    "reason": "short explanation"
}}
"""

        response = self.client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
        )

        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            return {
                "goal": "unknown",
                "reason": "The model returned invalid JSON.",
            }

    def select_tool(self, goal):
        """
        Map the goal to an approved backend tool.
        """

        goal_to_tool = {
            "maintenance_history": "get_maintenance_history",
            "available_technicians": "find_available_technicians",
            "appointment": "book_appointment",
        }

        tool_name = goal_to_tool.get(goal)

        if not tool_name:
            return None

        return self.tools.get(tool_name)

    def extract_parameters(self, goal, user_input):
        """
        Extract parameters from the user's request.

        This stage currently returns only the parameters
        that can safely be inferred from the conversation.
        """

        prompt = f"""
You are extracting parameters for a Smart Car Service system.

User request:
{user_input}

Detected goal:
{goal}

Return ONLY valid JSON.

For maintenance_history:
{{
    "car_id": null
}}

For available_technicians:
{{}}

For appointment:
{{
    "car_id": null,
    "technician_id": null,
    "service_type": null,
    "appointment_date": null,
    "appointment_time": null,
    "notes": ""
}}
"""

        response = self.client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
        )

        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            raise ValidationError(
                "The AI returned invalid parameters."
            )

    def execute_tool(self, tool, parameters):
        """
        Execute only an approved backend tool.
        """

        if tool is None:
            return {
                "success": False,
                "message": "No suitable tool was found.",
            }

        return tool(
            user=self.user,
            **parameters,
        )

    def observe(self, result):
        """
        Observe the tool result.
        """

        return result

    def complete(self, observation):
        """
        Return the final result.
        """

        return observation

    def run(self, user_input):
        """
        Execute the complete Agentic AI pipeline.
        """

        perception = self.perceive_goal(user_input)

        goal = perception.get("goal", "unknown")

        if goal == "unknown":
            return {
                "success": False,
                "message": "I could not determine what you want to do.",
            }

        tool = self.select_tool(goal)

        if tool is None:
            return {
                "success": False,
                "message": "No suitable tool is available.",
            }

        parameters = self.extract_parameters(
            goal,
            user_input,
        )

        result = self.execute_tool(
            tool,
            parameters,
        )

        observation = self.observe(result)

        return self.complete(observation)
    
    def choose_function(self, user_input):
        """
        Ask Gemini to choose one approved backend function.
        Gemini does not execute the function.
        """

        response = self.client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=user_input,
            config=types.GenerateContentConfig(
            tools=[
                types.Tool(
                    function_declarations=self.function_declarations
                )
            ],
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            ),
        ),
    )

        if not response.function_calls:
            return {
            "function_name": None,
            "arguments": {},
            "text": response.text,
        }

        function_call = response.function_calls[0]

        return {
        "function_name": function_call.name,
        "arguments": dict(function_call.args),
    }
        
    def execute_function_call(self, function_name, arguments):
        """
        Execute only functions that are explicitly registered
        in the Agent's tool whitelist.
        """

        if not function_name:
            return {
            "success": False,
            "message": "No function was requested.",
        }

        tool = self.tools.get(function_name)

        if tool is None:
            return {
            "success": False,
            "message": "Requested function is not allowed.",
        }

        try:
            result = tool(
            user=self.user,
            **arguments,
        )

            return {
            "success": True,
            "function_name": function_name,
            "result": result,
        }

        except ValidationError as exc:
            return {
            "success": False,
            "function_name": function_name,
            "message": str(exc),
        }    
            
    # def run_agent_loop(self, user_input):
    #     """
    #     Full Agentic AI loop.

    #     Gemini decides whether a backend tool is needed.
    #     The Agent executes only approved tools.
    #     The tool result is then returned to Gemini
    #     to generate the final natural-language response.
    #     """

    #     response = self.client.models.generate_content(
    #         model="gemini-3.5-flash-lite",
    #         contents=user_input,
    #         config=types.GenerateContentConfig(
    #         tools=[
    #             types.Tool(
    #                 function_declarations=self.function_declarations
    #             )
    #         ],
    #         automatic_function_calling=types.AutomaticFunctionCallingConfig(
    #             disable=True
    #         ),
    #     ),
    # )

    #     if not response.function_calls:
    #         return {
    #         "success": True,
    #         "tool_used": False,
    #         "answer": response.text,
    #     }

    #     function_call = response.function_calls[0]

    #     function_name = function_call.name
    #     arguments = dict(function_call.args)

    #     execution = self.execute_function_call(
    #     function_name,
    #     arguments,
    # )

    #     return {
    #     "success": execution["success"],
    #     "tool_used": True,
    #     "function_name": function_name,
    #     "arguments": arguments,
    #     "tool_result": execution,
    # }        
    
#     def run_agent_loop(self, user_input):
#         """
#         Full Agentic AI loop.

#         Flow:
#         User Input
#         -> Gemini Tool Selection
#         -> Approved Tool Execution
#         -> Tool Result
#         -> Gemini Final Answer
#         """

#         response = self.client.models.generate_content(
#             model="gemini-3.5-flash-lite",
#             contents=user_input,
#             config=types.GenerateContentConfig(
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

      
#         if not response.function_calls:
#             return {
#                 "success": True,
#                 "tool_used": False,
#                 "answer": response.text,
#             }


#         function_call = response.function_calls[0]

#         function_name = function_call.name
#         arguments = dict(function_call.args)

        
#         if self.requires_confirmation(function_name):
#             return self.build_confirmation_request(
#                 function_name,
#                 arguments,)
            
#         execution = self.execute_function_call(
#             function_name,
#             arguments,)

#         if not execution["success"]:
#             return {
#                 "success": False,
#                 "tool_used": True,
#                 "function_name": function_name,
#                 "arguments": arguments,
#                 "error": execution.get(
#                     "message",
#                     "Tool execution failed."
#                 ),
#             }


#         tool_result = execution["result"]

#         # if function_name == "check_appointment_slot":
#         #     if tool_result.get("available") is True:
#         #         return {
#         #             "success": True,
#         #             "tool_used": True,
#         #             "function_name": function_name,
#         #             "arguments": arguments,
#         #             "tool_result": tool_result,
#         #             "confirmation_required": True,
#         #             "next_action": "book_appointment",
#         #             "message": (
#         #                 "The appointment slot is available.\n\n"
#         #                 "Please confirm the following appointment:\n"
#         #                 f"- Technician: {tool_result['technician']['name']}\n"
#         #                 f"- Specialization: {tool_result['technician']['specialization']}\n"
#         #                 f"- Date: {tool_result['appointment_date']}\n"
#         #                 f"- Time: {tool_result['appointment_time']}\n\n"
#         #                 "Do you confirm this appointment?"
#         #             ),
#         #         }
#         if function_name == "check_appointment_slot":
#             if tool_result.get("available") is True:

#                 self.pending_action = {
#                     "function_name": "book_appointment",
#                     "arguments": {
#                         "car_id": arguments.get("car_id"),
#                         "technician_id": arguments.get("technician_id"),
#                         "service_type": arguments.get("service_type"),
#                         "appointment_date": arguments.get("appointment_date"),
#                         "appointment_time": arguments.get("appointment_time"),
#                         "notes": arguments.get("notes", ""),
#                     },
#                 }

#                 return {
#                     "success": True,
#                     "tool_used": True,
#                     "function_name": function_name,
#                     "arguments": arguments,
#                     "tool_result": tool_result,
#                     "confirmation_required": True,
#                     "next_action": "book_appointment",
#                     "message": (
#                         "The appointment slot is available.\n\n"
#                         "Please confirm the following appointment:\n"
#                         f"- Car ID: {arguments.get('car_id')}\n"
#                         f"- Technician: {tool_result['technician']['name']}\n"
#                         f"- Specialization: {tool_result['technician']['specialization']}\n"
#                         f"- Service: {arguments.get('service_type')}\n"
#                         f"- Date: {tool_result['appointment_date']}\n"
#                         f"- Time: {tool_result['appointment_time']}\n\n"
#                         "Do you confirm this appointment?"
#                     )
#                 }
                
#         final_prompt = f"""
# You are the final response generator for a Smart Car Service System.

# The user asked:
# {user_input}

# The backend tool that was executed:
# {function_name}

# The tool result is:
# {tool_result}

# Using only the tool result, provide a clear and concise
# answer to the user.

# Do not invent information.
# Do not mention internal tools, function calling,
# database, ORM, or implementation details.
# """

#         final_response = self.client.models.generate_content(
#             model="gemini-3.5-flash-lite",
#             contents=final_prompt,
#         )


#         return {
#             "success": True,
#             "tool_used": True,
#             "function_name": function_name,
#             "arguments": arguments,
#             "tool_result": tool_result,
#             "answer": final_response.text,
#         }

    def run_agent_loop(self, user_input):


        if self.pending_action:

            confirmation = user_input.strip().lower()

            if confirmation in [
            "yes",
            "y",
            "confirm",
            "confirmed",
            "approve",
            "ok",
            "okay",
        ]:

                result = self.confirm_pending_action(True)

                if result["success"]:

                    appointment = result["result"]["appointment"]

                    return {
                    "success": True,
                    "tool_used": True,
                    "function_name": "book_appointment",
                    "confirmation_required": False,
                    "answer": (
                        "Appointment booked successfully.\n\n"
                        f"Car: {appointment['car']}\n"
                        f"Technician: {appointment['technician']}\n"
                        f"Service: {appointment['service_type']}\n"
                        f"Date: {appointment['appointment_date']}\n"
                        f"Time: {appointment['appointment_time']}\n"
                        f"Status: {appointment['status']}"
                    ),
                }

                return {
                "success": False,
                "tool_used": True,
                "function_name": "book_appointment",
                "confirmation_required": False,
                "error": result.get(
                    "message",
                    "The appointment could not be booked.",
                ),
            }


            if confirmation in [
            "no",
            "n",
            "cancel",
            "cancelled",
            "decline",
            "reject",
        ]:

                    result = self.confirm_pending_action(False)

                    return {
                "success": True,
                "tool_used": False,
                "confirmation_required": False,
                "answer": result["message"],
            }


            return {
            "success": True,
            "tool_used": False,
            "confirmation_required": True,
            "pending_action": self.pending_action,
            "message": (
                "I have a pending appointment booking.\n\n"
                "Please reply with Yes to confirm or No to cancel."
            ),
        }


    

        booking_keywords = [
        "book",
        "booking",
        "appointment",
        "schedule",
        "reserve",
    ]

        is_booking_request = any(
        keyword in user_input.lower()
        for keyword in booking_keywords
    )


    

        if is_booking_request:

            booking_result = self.prepare_booking(user_input)

            if booking_result.get("success"):

                booking = booking_result["booking"]


            

                try:

                    car = Car.objects.get(
                    id=booking["car_id"]
                )

                except Car.DoesNotExist:

                    return {
                    "success": False,
                    "tool_used": True,
                    "error": "Car not found.",
                }


            
                is_staff_role = self.user.groups.filter(
                name__in=["Admin", "Manager"]).exists()


                if not is_staff_role and car.owner != self.user:

                    return {
                    "success": False,
                    "tool_used": True,
                    "error": (
                        "You do not have permission "
                        "to book an appointment for this car."
                    ),
                }


            

                slot_result = self.execute_function_call(
                "check_appointment_slot",
                {
                    "technician_id": booking["technician_id"],
                    "appointment_date": booking["appointment_date"],
                    "appointment_time": booking["appointment_time"],
                },
            )


                if not slot_result["success"]:

                    return {
                    "success": False,
                    "tool_used": True,
                    "function_name": "check_appointment_slot",
                    "error": slot_result.get(
                        "message",
                        "Could not check appointment availability.",
                    ),
                }


                tool_result = slot_result["result"]


            

                if not tool_result.get("available"):

                    return {
                    "success": True,
                    "tool_used": True,
                    "function_name": "check_appointment_slot",
                    "tool_result": tool_result,
                    "confirmation_required": False,
                    "answer": (
                        "The appointment slot is not available.\n\n"
                        f"Reason: "
                        f"{tool_result.get('reason', 'Unknown reason.')}"
                    ),
                }

                self.set_pending_booking(booking)


                return {
                "success": True,
                "tool_used": True,
                "function_name": "check_appointment_slot",
                "tool_result": tool_result,
                "confirmation_required": True,
                "next_action": "book_appointment",
                "pending_action": self.pending_action,
                "message": (
                    "The appointment slot is available.\n\n"
                    f"Car: {car.brand} {car.model}\n"
                    f"Car ID: {booking['car_id']}\n"
                    f"Technician: "
                    f"{tool_result['technician']['name']}\n"
                    f"Specialization: "
                    f"{tool_result['technician']['specialization']}\n"
                    f"Service: {booking['service_type']}\n"
                    f"Date: {booking['appointment_date']}\n"
                    f"Time: {booking['appointment_time']}\n\n"
                    "Do you confirm this appointment?"
                ),
            }


    # ============================================================
    # 4. Normal AI / Tool Selection
    # ============================================================

        response = self.client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=user_input,
        config=types.GenerateContentConfig(
            tools=[
                types.Tool(
                    function_declarations=self.function_declarations
                )
            ],
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            ),
        ),
    )




        if not response.function_calls:

            return {
            "success": True,
            "tool_used": False,
            "answer": response.text,
        }


        function_call = response.function_calls[0]

        function_name = function_call.name

        arguments = dict(function_call.args)



        if function_name == "check_appointment_slot":

            execution = self.execute_function_call(
            function_name,
            arguments,
        )


            if not execution["success"]:

                return {
                "success": False,
                "tool_used": True,
                "function_name": function_name,
                "arguments": arguments,
                "error": execution.get(
                    "message",
                    "Could not check the appointment slot.",
                ),
            }


            tool_result = execution["result"]


            if tool_result.get("available") is True:

                return {
                "success": True,
                "tool_used": True,
                "function_name": function_name,
                "arguments": arguments,
                "tool_result": tool_result,
                "confirmation_required": False,
                "answer": (
                    "The appointment slot is available.\n\n"
                    f"Technician: "
                    f"{tool_result['technician']['name']}\n"
                    f"Specialization: "
                    f"{tool_result['technician']['specialization']}\n"
                    f"Date: "
                    f"{tool_result['appointment_date']}\n"
                    f"Time: "
                    f"{tool_result['appointment_time']}"
                ),
            }


            return {
            "success": True,
            "tool_used": True,
            "function_name": function_name,
            "arguments": arguments,
            "tool_result": tool_result,
            "confirmation_required": False,
            "answer": (
                "The appointment slot is not available.\n\n"
                f"Reason: "
                f"{tool_result.get('reason', 'Unknown reason.')}"
            ),
        }


   

        if function_name == "book_appointment":

            return self.build_confirmation_request(
            function_name,
            arguments,
        )


    

        execution = self.execute_function_call(
        function_name,
        arguments,)


        if not execution["success"]:

            return {
            "success": False,
            "tool_used": True,
            "function_name": function_name,
            "arguments": arguments,
            "error": execution.get(
                "message",
                "Tool execution failed.",
            ),
        }


        tool_result = execution["result"]


    
        final_prompt = f"""
You are a Smart Car Service Assistant.

The user asked:
{user_input}

The backend tool that was executed:
{function_name}

Tool result:
{tool_result}

Answer the user clearly and concisely.

Do not invent information.
Only use information contained in the tool result.
"""


        final_response = self.client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=final_prompt,
    )


        return {
        "success": True,
        "tool_used": True,
        "function_name": function_name,
        "arguments": arguments,
        "tool_result": tool_result,
        "answer": final_response.text,
    }

                
        
    def requires_confirmation(self, function_name):
        """
        Return True for tools that perform actions
        that modify system data.
        """
        confirmation_required_tools = {
            "book_appointment",
        }

        return function_name in confirmation_required_tools   
    
    def build_confirmation_request(self, function_name, arguments):
        """
        Build a human-readable confirmation request
        before executing a destructive or state-changing action.
        """

        if function_name == "book_appointment":
            return {
                "confirmation_required": True,
                "function_name": function_name,
                "message": (
                    "Please confirm the following appointment:\n"
                    f"- Car ID: {arguments.get('car_id')}\n"
                    f"- Technician ID: {arguments.get('technician_id')}\n"
                    f"- Service: {arguments.get('service_type')}\n"
                    f"- Date: {arguments.get('appointment_date')}\n"
                    f"- Time: {arguments.get('appointment_time')}\n"
                    f"- Notes: {arguments.get('notes', '')}\n\n"
                    "Do you confirm this appointment?"
                ),
            }

        return {
            "confirmation_required": False,
        } 
        
    def prepare_booking(self, user_input):
        """
        Extract all information required for a booking
        without executing the booking.
        """

        response = self.client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=f"""
Extract the appointment booking information from the user's request.

User request:
{user_input}

Return ONLY valid JSON with this structure:

{{
    "car_id": integer,
    "technician_id": integer,
    "service_type": "string",
    "appointment_date": "YYYY-MM-DD",
    "appointment_time": "HH:MM",
    "notes": "string"
}}

Do not invent missing values.
If a value is not provided, use null.
""",
        )

        import json

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            return {
                "success": False,
                "message": "Could not extract valid booking information."
            }

        required_fields = [
            "car_id",
            "technician_id",
            "service_type",
            "appointment_date",
            "appointment_time",
        ]

        missing_fields = [
            field
            for field in required_fields
            if not data.get(field)
        ]

        if missing_fields:
            return {
                "success": False,
                "message": "Missing booking information.",
                "missing_fields": missing_fields,
            }

        return {
            "success": True,
            "booking": data,
        }    
        
    def set_pending_booking(self, booking):
        """
        Store a validated booking request waiting for user confirmation.
        """
        self.pending_action = {
        "function_name": "book_appointment",
        "arguments": {
            "car_id": booking["car_id"],
            "technician_id": booking["technician_id"],
            "service_type": booking["service_type"],
            "appointment_date": booking["appointment_date"],
            "appointment_time": booking["appointment_time"],
            "notes": booking.get("notes") or "",
        },
    }

        return self.pending_action 
    
    def confirm_pending_action(self, confirmed):
        """
        Execute the pending action only after explicit confirmation.
        """

        if not confirmed:
            self.pending_action = None

            return {
                "success": False,
                "confirmed": False,
                "message": "Appointment booking was cancelled."
            }

        if not self.pending_action:
            return {
                "success": False,
                "confirmed": False,
                "message": "There is no pending action to confirm."
            }

        function_name = self.pending_action["function_name"]
        arguments = self.pending_action["arguments"]

        execution = self.execute_function_call(
            function_name,
            arguments,
        )

        if not execution["success"]:
            return {
                "success": False,
                "confirmed": True,
                "message": execution.get(
                    "message",
                    "The appointment could not be booked."
                ),
            }

        self.pending_action = None

        return {
            "success": True,
            "confirmed": True,
            "function_name": function_name,
            "result": execution["result"],
        }   