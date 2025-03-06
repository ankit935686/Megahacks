from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import StudentResume, CareerRoadmap
import google.generativeai as genai
import logging
import PyPDF2
import io

# Set up logging
logger = logging.getLogger(__name__)

# Configure Gemini AI with your API key
genai.configure(api_key='AIzaSyBoSh27de1rMnal3wr7AGRuayGZxz06blg')

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')

@login_required
def upload_resume(request):
    """View for uploading resume files"""
    logger.info("Upload resume view accessed")
    if request.method == 'POST':
        logger.info("Processing POST request for resume upload")
        if 'resume_file' in request.FILES:
            resume_file = request.FILES['resume_file']
            logger.info(f"Resume file received: {resume_file.name}")
            
            try:
                # Extract text based on file type
                if resume_file.name.endswith('.pdf'):
                    # Read PDF file
                    pdf_reader = PyPDF2.PdfReader(io.BytesIO(resume_file.read()))
                    resume_text = ""
                    for page in pdf_reader.pages:
                        resume_text += page.extract_text()
                elif resume_file.name.endswith(('.doc', '.docx')):
                    # For now, handle doc/docx as text files
                    resume_text = resume_file.read().decode('utf-8', errors='ignore')
                else:
                    # Handle as plain text
                    resume_text = resume_file.read().decode('utf-8', errors='ignore')

                logger.info("Successfully extracted text from resume file")
                
                # Create resume object
                resume = StudentResume.objects.create(
                    user=request.user,
                    resume_text=resume_text
                )
                logger.info(f"Resume created successfully with ID: {resume.id}")
                
                return redirect('roadmap:generate_roadmap', resume_id=resume.id)
            except Exception as e:
                logger.error(f"Error processing resume file: {str(e)}")
                messages.error(request, f"Error processing resume: {str(e)}")
        else:
            logger.warning("No resume file provided in POST request")
            messages.error(request, "Please upload a resume file")
    return render(request, 'roadmap/upload_resume.html')

@login_required
def generate_roadmap(request, resume_id):
    """View for generating career roadmap from resume"""
    logger.info(f"Generate roadmap view accessed for resume_id: {resume_id}")
    try:
        resume = StudentResume.objects.get(id=resume_id, user=request.user)
        logger.info(f"Found resume for user: {request.user.username}")
        
        # Prepare prompt for Gemini AI
        prompt = f"""
        Based on the following resume, create a comprehensive career development roadmap with these sections:

        1. CAREER PROGRESSION PATH
           - Short-term goals (next 1-2 years)
           - Medium-term goals (3-5 years)
           - Long-term vision (5+ years)

        2. SKILL DEVELOPMENT PLAN
           - Technical skills to acquire or improve
           - Soft skills to develop
           - Priority order for skill acquisition

        3. RECOMMENDED CERTIFICATIONS & EDUCATION
           - Industry-specific certifications
           - Advanced degrees or specialized training
           - Timeline for completion

        4. LEARNING RESOURCES
           - Online courses and platforms
           - Books and publications
           - Professional training programs

        5. NETWORKING & PROFESSIONAL DEVELOPMENT
           - Industry events and conferences
           - Professional associations
           - Mentorship opportunities

        6. ADDITIONAL SUGGESTIONS
           - Career pivot opportunities
           - Industry trends to monitor
           - Alternative career paths

        RESUME:
        {resume.resume_text}

        Format your response with clear headings, bullet points, and concise recommendations. Be specific and actionable.
        """
        
        logger.info("Sending request to Gemini AI")
        try:
            # Generate response using Gemini AI
            response = model.generate_content(prompt)
            
            if hasattr(response, 'text'):
                roadmap_content = response.text
                logger.info("Successfully received response from Gemini AI")
                
                # Create suggestions section
                suggestions = """
                ADDITIONAL CAREER ENHANCEMENT SUGGESTIONS:
                
                1. Consider exploring adjacent fields that complement your current expertise
                2. Develop a personal brand through writing, speaking, or online presence
                3. Seek mentorship from industry leaders
                4. Participate in hackathons, competitions, or open-source projects
                5. Join professional communities and contribute regularly
                """
                
                # Create roadmap object
                roadmap = CareerRoadmap.objects.create(
                    user=request.user,
                    resume=resume,
                    roadmap_content=roadmap_content,
                    suggestions=suggestions
                )
                logger.info(f"Roadmap created successfully with ID: {roadmap.id}")
                
                return redirect('roadmap:view_roadmap', roadmap_id=roadmap.id)
            else:
                raise Exception("Invalid response format from Gemini AI")
            
        except Exception as e:
            logger.error(f"Error with Gemini AI: {str(e)}")
            messages.error(request, f"Error generating roadmap: {str(e)}")
            return redirect('roadmap:upload_resume')

    except StudentResume.DoesNotExist:
        logger.error(f"Resume not found with ID: {resume_id}")
        messages.error(request, 'Resume not found.')
        return redirect('roadmap:upload_resume')
    except Exception as e:
        logger.error(f"Unexpected error in generate_roadmap: {str(e)}")
        messages.error(request, f'Error generating roadmap: {str(e)}')
        return redirect('roadmap:upload_resume')

@login_required
def view_roadmap(request, roadmap_id):
    """View for displaying generated roadmap"""
    logger.info(f"View roadmap accessed for roadmap_id: {roadmap_id}")
    try:
        roadmap = CareerRoadmap.objects.get(id=roadmap_id, user=request.user)
        logger.info(f"Found roadmap for user: {request.user.username}")
        context = {
            'roadmap': roadmap,
            'resume': roadmap.resume
        }
        logger.info("Rendering view_roadmap.html template")
        return render(request, 'roadmap/view_roadmap.html', context)
    except CareerRoadmap.DoesNotExist:
        logger.error(f"Roadmap not found with ID: {roadmap_id}")
        messages.error(request, 'Roadmap not found.')
        return redirect('roadmap:upload_resume')
    except Exception as e:
        logger.error(f"Unexpected error in view_roadmap: {str(e)}")
        messages.error(request, f'Error viewing roadmap: {str(e)}')
        return redirect('roadmap:upload_resume')
