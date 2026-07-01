from flask import Flask, render_template, abort

app = Flask(__name__)

# Mock Database for Services
services_data = {
    1: {
        "id": 1,
        "name": "Signature Cuts",
        "desc": "Precision cuts tailored to your unique facial structure and hair type.",
        "price": 95,
        "image": "https://images.unsplash.com/photo-1560066984-138dadb4c035?q=80&w=600",
        "category": "cuts",
        "sub_works": ["Women's Design Cut & Blowdry", "Men's Classic Shear Cut", "Bang & Fringe Trim", "Kids' Stylist Cut (Under 10)"],
        "details": "Every signature cut begins with a detailed personal consultation, followed by a relaxing shampoo, scalp massage, and custom conditioning. Your stylist will then perform a precision shear or razor cut finished with a premium blowout and styling advice for home care."
    },
    2: {
        "id": 2,
        "name": "Balayage & Color",
        "desc": "Bespoke color transformations, highlights, and glosses using organic formulas.",
        "price": 210,
        "image": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?q=80&w=600",
        "category": "color",
        "sub_works": ["Full Hand-Painted Balayage", "Dimensional Foil Highlights", "All-Over Gloss & Tone", "Grey Coverage Root Retouch"],
        "details": "Our master colorists specialize in painting high-dimension balayage and placing strategic highlights that blend seamlessly as they grow out. We utilize advanced color bonding treatments to protect hair structure and locking gloss to seal vibrant shine."
    },
    3: {
        "id": 3,
        "name": "Styling & Blowouts",
        "desc": "Flawless blowouts, sleek straightening, bouncy waves, and structured up-dos.",
        "price": 65,
        "image": "https://images.unsplash.com/photo-1595425970377-c9703cf48b6d?q=80&w=600",
        "category": "styling",
        "sub_works": ["Signature Bouncy Blowout", "Sleek Silk Press", "Beach Waves & Curls", "Special Event Structured Updo"],
        "details": "Prepare for any occasion or elevate your weekly routine with our styling sessions. We use luxury heat protection and volume serums, styling with premium Dyson tools to achieve high shine and long-lasting bounce."
    },
    4: {
        "id": 4,
        "name": "Hair Treatments",
        "desc": "Deep nourishment, keratin smoothing, and revitalizing scalp therapies.",
        "price": 80,
        "image": "https://images.unsplash.com/photo-1517832606589-7a598bbd425c?q=80&w=600",
        "category": "treatments",
        "sub_works": ["Deep Conditioning Hydration Mask", "Keratin Smoothing Therapy", "Scalp Detoxification Treatment", "Olaplex Bonding Repair Therapy"],
        "details": "Revive dull, damaged, or frizzy hair with our advanced clinical treatments. We analyze scalp health and hair density to apply targeted nutrition, repairing broken bonds and infusing intense moisture for a silky touch."
    }
}

# Mock Database for Team Members
team_data = {
    1: {
        "id": 1,
        "name": "Sarah Jenkins",
        "role": "Founder & Master Stylist",
        "image": "https://images.unsplash.com/photo-1580489944761-15a19d654956?q=80&w=400",
        "bio": "Sarah trained at the prestigious Vidal Sassoon Academy in London and spent a decade working in Paris before founding Vision Salon. Her precision cutting styles and warm consultations have earned her a loyal Beverly Hills clientele.",
        "specialties": ["Precision Shear Cuts", "French Balayage", "Bridal & Editorial Styling"],
        "hours": "Tue - Fri: 9:00 AM - 5:00 PM, Sat: 9:00 AM - 6:00 PM",
        "years_exp": 15
    },
    2: {
        "id": 2,
        "name": "Michael Chang",
        "role": "Master Color Specialist",
        "image": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?q=80&w=400",
        "bio": "With an eye for dimension and light, Michael spent years styling backstage at New York Fashion Week. He is known for crafting sun-kissed blonde tones, vibrant highlights, and rich multidimensional brunettes while maintaining hair health.",
        "specialties": ["Custom Highlight Placement", "Color Corrections", "Vibrant Fashion Tones"],
        "hours": "Wed - Sat: 10:00 AM - 7:00 PM",
        "years_exp": 10
    },
    3: {
        "id": 3,
        "name": "Amanda Ross",
        "role": "Texture & Styling Expert",
        "image": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=400",
        "bio": "Amanda is passionate about celebrating natural curls and textures. She specializes in dry cutting curls, installing protective styles, and prescribing custom scalp therapies to establish a strong, healthy foundation for hair.",
        "specialties": ["Dry Deva-Cuts", "Natural Texture Therapy", "Scalp Wellness Treatments"],
        "hours": "Mon - Thu: 9:00 AM - 6:00 PM",
        "years_exp": 8
    }
}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/services')
def services():
    return render_template("services.html", services=services_data.values())

@app.route('/services/<int:service_id>')
def service_detail(service_id):
    service = services_data.get(service_id)
    if not service:
        abort(404)
    # Samples: all other services
    samples = [s for s in services_data.values() if s['id'] != service_id]
    return render_template("service_detail.html", service=service, samples=samples)

@app.route('/story')
def story():
    return render_template("story.html", team=team_data.values())

@app.route('/team')
def team():
    return render_template("team.html", team=team_data.values())

@app.route('/team/<int:member_id>')
def team_detail(member_id):
    member = team_data.get(member_id)
    if not member:
        abort(404)
    return render_template("team_detail.html", member=member)

@app.route('/gallery')
def gallery():
    return render_template("gallery.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/book')
def book():
    return render_template("book.html", services=services_data.values(), team=team_data.values())

if __name__ == '__main__':
    app.run(debug=True)