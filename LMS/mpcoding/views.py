from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CodeSubmission, Room, Battle, CodingQuestion
from django.http import JsonResponse
from .code_executor import execute_code
from .utils.gemini_api import generate_coding_question
import json
import requests
from django.urls import reverse
from .utils.code_evaluator import evaluate_code_with_test_cases

# Create your views here.

@login_required
def code_editor(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        language = request.POST.get('language')
        
        # Execute the code
        result = execute_code(code, language)
        
        # Save the submission
        submission = CodeSubmission.objects.create(
            user=request.user,
            code=code,
            language=language,
            output=result['output'],
            error=result['error'],
            execution_time=result['execution_time']
        )
        
        return JsonResponse({
            'status': 'success',
            'output': result['output'],
            'error': result['error'],
            'execution_time': result['execution_time']
        })
    
    return render(request, 'mpcoding/editor.html')

@login_required
def create_room(request):
    room = Room.objects.create(player1=request.user)
    return redirect('mpcoding:wait_room', room_id=room.room_id)

@login_required
def join_room(request, room_id):
    room = get_object_or_404(Room, room_id=room_id, is_active=True)
    
    if not room.player2 and room.player1 != request.user:
        room.player2 = request.user
        room.save()
        return redirect('mpcoding:battle_room', room_id=room_id)
    
    return redirect('mpcoding:battle_room', room_id=room_id)

@login_required
def wait_room(request, room_id):
    room = get_object_or_404(Room, room_id=room_id)
    return render(request, 'mpcoding/wait_room.html', {'room': room})

@login_required
def battle_room(request, room_id):
    room = get_object_or_404(Room, room_id=room_id)
    try:
        battle = Battle.objects.get(room=room)
    except Battle.DoesNotExist:
        # If battle doesn't exist, redirect to wait room
        if request.user == room.player1:
            return redirect('mpcoding:wait_room', room_id=room_id)
        else:
            # Generate question and create battle when accessing battle room
            question_data = generate_coding_question('medium')
            question = CodingQuestion.objects.create(
                title=question_data['title'],
                description=question_data['description'],
                test_cases=question_data['test_cases'],
                difficulty='medium'
            )
            battle = Battle.objects.create(room=room, question=question)
    
    context = {
        'room': room,
        'battle': battle,
        'is_player1': request.user == room.player1
    }
    return render(request, 'mpcoding/battle_room.html', context)

@login_required
def submit_code(request, room_id):
    if request.method == 'POST':
        try:
            room = get_object_or_404(Room, room_id=room_id)
            battle = Battle.objects.get(room=room)
            code = request.POST.get('code')
            language = request.POST.get('language', 'python')
            
            print(f"Debug: Processing submission for {request.user.username}")  # Debug log
            print(f"Debug: Question function name: {battle.question.function_name}")  # Debug log
            
            # Use code_evaluator with function name
            test_results = evaluate_code_with_test_cases(
                code, 
                language, 
                battle.question.test_cases,
                battle.question.function_name  # Pass function name
            )
            
            # Store code submission and results
            if request.user == room.player1:
                battle.player1_code = code
                battle.player1_completed = True
                battle.player1_results = test_results
            else:
                battle.player2_code = code
                battle.player2_completed = True
                battle.player2_results = test_results
            
            battle.save()
            
            # If both players have submitted, determine winner
            if battle.player1_completed and battle.player2_completed:
                determine_winner(battle)
                room.is_active = False
                room.save()
            
            return JsonResponse({
                'status': 'success',
                'redirect_url': reverse('mpcoding:battle_result', args=[room_id])
            })
        except Exception as e:
            print(f"Debug: Error in submit_code: {str(e)}")  # Debug log
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    })

def determine_winner(battle):
    """Determine the winner based on test case results"""
    p1_score = sum(1 for result in battle.player1_results if result.get('passed', False))
    p2_score = sum(1 for result in battle.player2_results if result.get('passed', False))
    
    print(f"Player 1 score: {p1_score}, Player 2 score: {p2_score}")  # Debug print
    
    if p1_score > p2_score:
        battle.winner = battle.room.player1
    elif p2_score > p1_score:
        battle.winner = battle.room.player2
    # If scores are equal, winner remains None (tie)
    
    battle.save()

@login_required
def battle_result(request, room_id):
    room = get_object_or_404(Room, room_id=room_id)
    battle = Battle.objects.get(room=room)
    
    # Debug prints
    print(f"Player 1 results: {battle.player1_results}")
    print(f"Player 2 results: {battle.player2_results}")
    print(f"Winner: {battle.winner}")
    
    context = {
        'room': room,
        'battle': battle,
        'winner': battle.winner,
        'is_player1': request.user == room.player1
    }
    return render(request, 'mpcoding/battle_result.html', context)

@login_required
def check_room(request, room_id):
    room = get_object_or_404(Room, room_id=room_id)
    return JsonResponse({
        'started': room.player2 is not None
    })

@login_required
def check_battle(request, room_id):
    battle = get_object_or_404(Battle, room__room_id=room_id)
    return JsonResponse({
        'completed': battle.player1_completed and battle.player2_completed
    })
