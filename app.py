import os
import io
from PIL import Image
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
# That's How You Edit Your Code and Redeploy
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default-secret-key')

COURSE_VIDEOS = [
    {
        "id": "video_1",
        "module": "PART 1",
        "title": "Introduction",
        "duration": "22:00",
        "thumbnail": "https://img.youtube.com/vi/AB3st2n1-B0/hqdefault.jpg",
        "url": "https://www.youtube.com/embed/AB3st2n1-B0",
        "description": "Introduction to the course."
    },
    {
        "id": "video_2",
        "module": "PART 2",
        "title": "Drafting using AI Website Builder",
        "duration": "32:55",
        "thumbnail": "https://img.youtube.com/vi/_vQOWtgYBsg/hqdefault.jpg",
        "url": "https://www.youtube.com/embed/_vQOWtgYBsg",
        "description": "Learn how to draft your website using an AI builder."
    },
    {
        "id": "video_3",
        "module": "PART 3",
        "title": "Setup of Your PC for Coding",
        "duration": "21:43",
        "thumbnail": "https://img.youtube.com/vi/Vqog0UA-kO0/hqdefault.jpg",
        "url": "https://www.youtube.com/embed/Vqog0UA-kO0",
        "description": "Getting your local environment ready for coding."
    },
    {
        "id": "video_4",
        "module": "PART 4",
        "title": "Coding using AI",
        "duration": "35:47",
        "thumbnail": "https://img.youtube.com/vi/p0-cJCyZ6t0/hqdefault.jpg",
        "url": "https://www.youtube.com/embed/p0-cJCyZ6t0",
        "description": "Using generative AI to write code."
    },
    {
        "id": "video_5",
        "module": "PART 5",
        "title": "Manual Coding for Customization",
        "duration": "15:30",
        "thumbnail": "https://img.youtube.com/vi/J0RYs3CK2Aw/hqdefault.jpg",
        "url": "https://www.youtube.com/embed/J0RYs3CK2Aw",
        "description": "Fine-tuning your code manually."
    },
    {
        "id": "video_6",
        "module": "PART 6",
        "title": "Deployment of Website",
        "duration": "10:00",
        "thumbnail": "https://img.youtube.com/vi/w_Y4XLZI9a4/hqdefault.jpg",
        "url": "https://www.youtube.com/embed/w_Y4XLZI9a4",
        "description": "Deploy your website to the internet."
    },
    {
        "id": "video_7",
        "module": "PART 7",
        "title": "Personal Website Demo",
        "duration": "4:20",
        "thumbnail": "https://img.youtube.com/vi/jNQXAC9IVRw/hqdefault.jpg",
        "url": "https://www.youtube.com/embed/jNQXAC9IVRw",
        "description": "A demo of the finished personal website."
    }
]

COURSE_SLIDES = [
    {
        "id": "slide_1",
        "module": "PART 1",
        "title": "Introduction",
        "images": [
            "images/deck_1/1.jpg",
            "images/deck_1/2.jpg",
            "images/deck_1/3.jpg",
            "images/deck_1/4.jpg",
            "images/deck_1/5.jpg",
            "images/deck_1/6.jpg",
            "images/deck_1/7.jpg",
            "images/deck_1/8.jpg",
            "images/deck_1/9.jpg",
            "images/deck_1/10.jpg",
            "images/deck_1/11.jpg"
        ]
    },
    {
        "id": "slide_2",
        "module": "PART 2",
        "title": "Drafting using AI Website Builder",
        "images": [
            "images/deck_2/1.jpg",
            "images/deck_2/2.jpg",
            "images/deck_2/3.jpg",
            "images/deck_2/4.jpg",
            "images/deck_2/5.jpg",
            "images/deck_2/6.jpg",
            "images/deck_2/7.jpg",
            "images/deck_2/8.jpg",
            "images/deck_2/9.jpg",
            "images/deck_2/10.jpg",
            "images/deck_2/11.jpg",
            "images/deck_2/12.jpg"
        ]
    },
    {
        "id": "slide_3",
        "module": "PART 3",
        "title": "Setup of Your PC for Coding",
        "images": [
            "images/deck_3/1.jpg",
            "images/deck_3/2.jpg",
            "images/deck_3/3.jpg",
            "images/deck_3/4.jpg",
            "images/deck_3/5.jpg",
            "images/deck_3/6.jpg",
            "images/deck_3/7.jpg",
            "images/deck_3/8.jpg"
        ]
    },
    {
        "id": "slide_4",
        "module": "PART 4",
        "title": "Coding using AI",
        "images": [
            "images/deck_4/1.jpg",
            "images/deck_4/2.jpg",
            "images/deck_4/3.jpg",
            "images/deck_4/4.jpg",
            "images/deck_4/5.jpg",
            "images/deck_4/6.jpg",
            "images/deck_4/7.jpg",
            "images/deck_4/8.jpg",
            "images/deck_4/9.jpg",
            "images/deck_4/10.jpg",
            "images/deck_4/11.jpg",
            "images/deck_4/12.jpg",
            "images/deck_4/13.jpg",
            "images/deck_4/14.jpg",
            "images/deck_4/15.jpg",
            "images/deck_4/16.jpg",
            "images/deck_4/17.jpg",
            "images/deck_4/18.jpg",
            "images/deck_4/19.jpg",
            "images/deck_4/20.jpg",
            "images/deck_4/21.jpg",
            "images/deck_4/22.jpg",
            "images/deck_4/23.jpg",
            "images/deck_4/24.jpg",
            "images/deck_4/25.jpg",
            "images/deck_4/26.jpg",
            "images/deck_4/27.jpg",
            "images/deck_4/28.jpg",
            "images/deck_4/29.jpg"
        ]
    },
    {
        "id": "slide_5",
        "module": "PART 5",
        "title": "Manual Coding for Customization",
        "images": [
            "images/deck_5/1.jpg",
            "images/deck_5/2.jpg",
            "images/deck_5/3.jpg",
            "images/deck_5/4.jpg",
            "images/deck_5/5.jpg",
            "images/deck_5/6.jpg",
            "images/deck_5/7.jpg",
            "images/deck_5/8.jpg",
            "images/deck_5/9.jpg",
            "images/deck_5/10.jpg",
            "images/deck_5/11.jpg",
            "images/deck_5/12.jpg",
            "images/deck_5/13.jpg",
            "images/deck_5/14.jpg",
            "images/deck_5/15.jpg",
            "images/deck_5/16.jpg",
            "images/deck_5/17.jpg",
            "images/deck_5/18.jpg",
            "images/deck_5/19.jpg",
            "images/deck_5/20.jpg",
            "images/deck_5/21.jpg",
            "images/deck_5/22.jpg",
            "images/deck_5/23.jpg",
            "images/deck_5/24.jpg",
            "images/deck_5/25.jpg",
            "images/deck_5/26.jpg",
            "images/deck_5/27.jpg",
            "images/deck_5/28.jpg",
            "images/deck_5/29.jpg",
            "images/deck_5/30.jpg",
            "images/deck_5/31.jpg",
            "images/deck_5/32.jpg",
            "images/deck_5/33.jpg",
            "images/deck_5/34.jpg",
            "images/deck_5/35.jpg"
        ]
    },
    {
        "id": "slide_6",
        "module": "PART 6",
        "title": "Deployment of Website",
        "images": [
            "images/deck_6/1.jpg",
            "images/deck_6/2.jpg",
            "images/deck_6/3.jpg",
            "images/deck_6/4.jpg",
            "images/deck_6/5.jpg",
            "images/deck_6/6.jpg",
            "images/deck_6/7.jpg",
            "images/deck_6/8.jpg",
            "images/deck_6/9.jpg",
            "images/deck_6/10.jpg",
            "images/deck_6/11.jpg",
            "images/deck_6/12.jpg",
            "images/deck_6/13.jpg",
            "images/deck_6/14.jpg",
            "images/deck_6/15.jpg",
            "images/deck_6/16.jpg",
            "images/deck_6/17.jpg",
            "images/deck_6/18.jpg",
            "images/deck_6/19.jpg",
            "images/deck_6/20.jpg",
            "images/deck_6/21.jpg",
            "images/deck_6/22.jpg",
            "images/deck_6/23.jpg"
        ]
    },
    {
        "id": "slide_7",
        "module": "PART 7",
        "title": "Personal Website Demo",
        "images": [
        ]
    }
]

# Supabase Initialization
url: str = os.environ.get("SUPABASE_URL", "").strip().strip('"').strip("'")
key: str = os.environ.get("SUPABASE_KEY", "").strip().strip('"').strip("'")

print("=== DEBUG INFO ===")
print(f"URL: {url}")
print(f"KEY LENGTH: {len(key)}")
print(f"KEY STARTS WITH: {key[:15] if len(key) > 15 else key}")
print("==================")

supabase: Client = None
if url and key:
    try:
        supabase = create_client(url, key)
    except Exception as e:
        print(f"SUPABASE CRASHED: {e}")

supabase: Client = None
if url and key:
    supabase = create_client(url, key)

# Helper to require login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Helper to require completed profile
def profile_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        
        user_id = session['user'].get('id')
        if supabase:
            try:
                response = supabase.table('user_profiles').select('profile_completed').eq('id', user_id).execute()
                if not response.data or not response.data[0].get('profile_completed'):
                    flash("Please complete your profile to access the tutorials.")
                    return redirect(url_for('settings'))
            except Exception as e:
                print(f"Error checking profile: {e}")
                
        return f(*args, **kwargs)
    return decorated_function

# Context processor to inject user into all templates
@app.context_processor
def inject_user():
    user = session.get('user')
    profile = None
    if user and supabase:
        try:
            res = supabase.table('user_profiles').select('*').eq('id', user['id']).execute()
            if res.data:
                profile = res.data[0]
                
            # Also get video stats
            prog_res = supabase.table('video_progress').select('*', count='exact').eq('user_id', user['id']).execute()
            completed_count = len(prog_res.data) if prog_res.data else 0
            if profile:
                profile['completed_videos_count'] = completed_count
        except Exception as e:
            print(f"Error fetching profile context: {e}")
            
    return dict(user=user, profile=profile)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not supabase:
            flash("Supabase not configured. Login unavailable.")
            return render_template('login.html')
            
        try:
            response = supabase.auth.sign_in_with_password({"email": email, "password": password})
            session['user'] = response.user.model_dump()
            return redirect(url_for('index'))
        except Exception as e:
            flash(str(e))
            
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user' in session:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash("Passwords do not match.")
            return render_template('signup.html')
            
        if not supabase:
            flash("Supabase not configured. Signup unavailable.")
            return render_template('signup.html')
            
        try:
            response = supabase.auth.sign_up({
                "email": email, 
                "password": password,
                "options": {
                    "data": {
                        "full_name": full_name
                    }
                }
            })
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            flash(str(e))
            
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    if supabase:
        supabase.auth.sign_out()
    return redirect(url_for('index'))

@app.route('/videos', defaults={'video_id': None})
@app.route('/videos/<video_id>')
@profile_required
def videos(video_id):
    user_id = session['user']['id']
    completed_video_ids = []
    if supabase:
        try:
            res = supabase.table('video_progress').select('video_id').eq('user_id', user_id).execute()
            if res.data:
                completed_video_ids = [row['video_id'] for row in res.data]
        except Exception as e:
            print(f"Error fetching video progress: {e}")
            
    unlocked_video_ids = []
    
    # Calculate unlocked videos (sequential)
    for i, video in enumerate(COURSE_VIDEOS):
        if i == 0 or COURSE_VIDEOS[i-1]['id'] in completed_video_ids:
            unlocked_video_ids.append(video['id'])
        else:
            break
            
    # Default to the first video
    if not video_id:
        return redirect(url_for('videos', video_id=COURSE_VIDEOS[0]['id']))
        
    current_video = next((v for v in COURSE_VIDEOS if v['id'] == video_id), COURSE_VIDEOS[0])
    
    if video_id not in unlocked_video_ids:
        flash("You need to complete the previous videos to unlock this one.")
        return redirect(url_for('videos'))
        
    return render_template('videos.html', 
                           course_videos=COURSE_VIDEOS, 
                           current_video=current_video, 
                           completed_video_ids=completed_video_ids,
                           unlocked_video_ids=unlocked_video_ids)

@app.route('/slides', defaults={'slide_id': None})
@app.route('/slides/<slide_id>')
@profile_required
def slides(slide_id):
    if not slide_id:
        return redirect(url_for('slides', slide_id=COURSE_SLIDES[0]['id']))
        
    current_slide = next((s for s in COURSE_SLIDES if s['id'] == slide_id), COURSE_SLIDES[0])
    current_index = next((i for i, s in enumerate(COURSE_SLIDES) if s['id'] == current_slide['id']), 0)
    
    prev_slide = COURSE_SLIDES[current_index - 1] if current_index > 0 else None
    next_slide = COURSE_SLIDES[current_index + 1] if current_index < len(COURSE_SLIDES) - 1 else None
    
    return render_template('slides.html', 
                           course_slides=COURSE_SLIDES,
                           current_slide=current_slide,
                           current_index=current_index,
                           prev_slide=prev_slide,
                           next_slide=next_slide)

@app.route('/slides/<slide_id>/download')
@profile_required
def download_deck(slide_id):
    current_slide = next((s for s in COURSE_SLIDES if s['id'] == slide_id), None)
    if not current_slide or not current_slide.get('images'):
        flash("No images available for this deck.")
        return redirect(url_for('slides', slide_id=slide_id))
    
    image_paths = current_slide['images']
    pil_images = []
    
    for img_path in image_paths:
        abs_path = os.path.join(app.root_path, 'static', img_path)
        if os.path.exists(abs_path):
            img = Image.open(abs_path)
            # Convert to RGB to avoid issues with transparency when saving as PDF
            if img.mode != 'RGB':
                img = img.convert('RGB')
            pil_images.append(img)
            
    if not pil_images:
        flash("Could not generate PDF (images not found).")
        return redirect(url_for('slides', slide_id=slide_id))
        
    pdf_bytes = io.BytesIO()
    
    if len(pil_images) == 1:
        pil_images[0].save(pdf_bytes, format='PDF', resolution=100.0)
    else:
        pil_images[0].save(pdf_bytes, format='PDF', resolution=100.0, save_all=True, append_images=pil_images[1:])
        
    pdf_bytes.seek(0)
    return send_file(
        pdf_bytes,
        download_name=f"{current_slide['title'].replace(' ', '_')}.pdf",
        as_attachment=True,
        mimetype='application/pdf'
    )

@app.route('/worksheet')
@profile_required
def worksheet():
    return render_template('worksheet.html')

@app.route('/profile')
@login_required
def profile():
    user_id = session['user']['id']
    worksheets = []
    if supabase:
        try:
            res = supabase.table('worksheets').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(3).execute()
            if res.data:
                worksheets = res.data
        except Exception as e:
            print(f"Error fetching worksheets for profile: {e}")
            
    return render_template('profile.html', worksheets=worksheets)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST' and supabase:
        user_id = session['user']['id']
        full_name = request.form.get('full_name')
        avatar_url = request.form.get('avatar_url')
        university = request.form.get('university')
        major = request.form.get('major')
        short_bio = request.form.get('short_bio')
        
        # Check if they have provided enough info to complete profile
        profile_completed = bool(university and short_bio)
        
        try:
            # Upsert user profile data
            data = {
                "id": user_id,
                "full_name": full_name,
                "avatar_url": avatar_url,
                "university": university,
                "major": major,
                "short_bio": short_bio,
                "profile_completed": profile_completed
            }
            supabase.table('user_profiles').upsert(data).execute()
            
            flash("Profile updated successfully!", "success")
            if profile_completed:
                return redirect(url_for('videos'))
        except Exception as e:
            flash(f"Error updating profile: {str(e)}")
            
    return render_template('settings.html')

@app.route('/settings/security', methods=['POST'])
@login_required
def update_security():
    if not supabase:
        flash("Supabase not configured.")
        return redirect(url_for('settings'))
    
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if new_password != confirm_password:
        flash("New passwords do not match.")
        return redirect(url_for('settings') + "#security")
        
    try:
        supabase.auth.update_user({"password": new_password})
        flash("Password updated successfully!", "success")
    except Exception as e:
        flash(f"Error updating password: {str(e)}")
        
    return redirect(url_for('settings') + "#security")

@app.route('/settings/email', methods=['POST'])
@login_required
def update_email():
    if not supabase:
        flash("Supabase not configured.")
        return redirect(url_for('settings'))
        
    new_email = request.form.get('new_email')
    
    try:
        res = supabase.auth.update_user({"email": new_email})
        session['user'] = res.user.model_dump()
        flash("Email updated successfully!", "success")
    except Exception as e:
        flash(f"Error updating email: {str(e)}")
        
    return redirect(url_for('settings') + "#email")
@app.route('/api/complete_video', methods=['POST'])
@login_required
def complete_video():
    if not supabase:
        return jsonify({"success": False, "error": "Supabase not configured"})
        
    user_id = session['user']['id']
    data = request.get_json()
    video_id = data.get('video_id')
    
    if not video_id:
        return jsonify({"success": False, "error": "Missing video_id"})
        
    try:
        # Record video progress
        supabase.table('video_progress').insert({
            "user_id": user_id,
            "video_id": video_id
        }).execute()
        
        # Count total completed videos
        res = supabase.table('video_progress').select('*', count='exact').eq('user_id', user_id).execute()
        total_videos = len(res.data) if res.data else 0
        
        # Update technical skill level based on progress
        new_level = "Beginner"
        if total_videos >= 5:
            new_level = "Advanced"
        elif total_videos >= 3:
            new_level = "Intermediate"
            
        supabase.table('user_profiles').update({"python_level": new_level}).eq('id', user_id).execute()
        
        return jsonify({
            "success": True, 
            "total_completed": total_videos,
            "new_level": new_level
        })
    except Exception as e:
        # Might fail if video already completed (unique constraint)
        return jsonify({"success": False, "error": str(e)})

@app.route('/worksheet/history')
@profile_required
def worksheet_history():
    user_id = session['user']['id']
    worksheets = []
    if supabase:
        try:
            res = supabase.table('worksheets').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
            if res.data:
                worksheets = res.data
        except Exception as e:
            print(f"Error fetching worksheets: {e}")
            flash("Unable to load worksheet history at this time.")
    
    return render_template('worksheet_history.html', worksheets=worksheets)

@app.route('/api/worksheets', methods=['POST'])
@login_required
def save_worksheet():
    if not supabase:
        return jsonify({"success": False, "error": "Database not configured"})
        
    user_id = session['user']['id']
    data = request.get_json()
    
    try:
        payload = {
            "user_id": user_id,
            "purpose": data.get("purpose", ""),
            "target_user": data.get("target_user", ""),
            "mission": data.get("mission", ""),
            "nav_features": data.get("nav_features", []),
            "auth_features": data.get("auth_features", []),
            "footer_features": data.get("footer_features", []),
            "pages": data.get("pages", []),
            "generated_prompt": data.get("generated_prompt", "")
        }
        
        res = supabase.table('worksheets').insert(payload).execute()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# Vercel needs app to be exposed
if __name__ == '__main__':
    app.run(debug=True)
