from . import main
from flask import render_template, jsonify
from app.models.gallery_model import GalleryModel


@main.route('/gallery')
def gallery():
    try:
        galleries_db = GalleryModel.query.order_by(GalleryModel.id).all()
        galleries = [g.json() for g in galleries_db]

        categories = sorted(list({g['category'] for g in galleries}))

        patterns = [
            ['left-top', 'left-bottom', 'right-tall'],
            ['left-tall', 'right-top', 'right-bottom'],
            ['left-top', 'left-bottom', 'right-tall'],
        ]

        blocks = []
        i = 0
        total = len(galleries)
        for patt in patterns:
            slots = []
            for slot_name in patt:
                if i < total:
                    item = galleries[i].copy()
                    item['layout'] = slot_name
                    slots.append(item)
                    i += 1
            if slots:
                blocks.append({'pattern': patt, 'slots': slots})

        while i < total:
            item = galleries[i].copy()
            item['layout'] = 'single'
            blocks.append({'pattern': ['single'], 'slots': [item]})
            i += 1

        return render_template('gallery.html', blocks=blocks, categories=categories)
    except Exception as e:
        print('Error fetching gallery data:', e)
        return jsonify({"error": "Failed to fetch gallery data"})
