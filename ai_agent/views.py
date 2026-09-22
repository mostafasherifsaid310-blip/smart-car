from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from .agent import SmartCarAgent


@login_required
def chat_view(request):

    if request.method == "GET":
        return render(request, "ai_agent/chat.html")


    if request.method == "POST":

        user_message = request.POST.get("message", "").strip()

        if not user_message:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Message is required.",
                },
                status=400,
            )


        agent = SmartCarAgent(user=request.user)


        pending_action = request.session.get("ai_pending_action")
        
        # print("SESSION PENDING ACTION:", pending_action)

        if pending_action:
            agent.pending_action = pending_action


        result = agent.run_agent_loop(user_message)
        
        # print("AGENT PENDING ACTION:", agent.pending_action)


        if agent.pending_action:

            request.session["ai_pending_action"] = agent.pending_action

            request.session.modified = True

        else:

            request.session.pop("ai_pending_action", None)

            request.session.modified = True
            
        # print("SESSION AFTER SAVE:", request.session.get("ai_pending_action"))    


        return JsonResponse(result)


    return JsonResponse(
        {
            "success": False,
            "error": "Method not allowed.",
        },
        status=405,
    )