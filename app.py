from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Reel advice from Dr. Ahmed
advice_quotes = [
    "Even on the darkest screens, there's light.",
    "Sometimes movies say what words cannot.",
    "You’re not alone. That’s why stories exist.",
    "Reel therapy is real therapy.",
    "Let your heart feel every frame."
]

# Color themes for each mood
mood_colors = {
    "happy": "#ffd93d",
    "sad": "#87ceeb",
    "anxious": "#ffb3c1",
    "angry": "#ff6b6b",
    "heartbroken": "#c08497",
    "burntout": "#a0a0a0",
    "inlove": "#f78fb3",
    "nostalgic": "#f5deb3"
}

# Movie recommendations by mood (no images, just title + note)
moods = {
    "sad": [
        {"title": "Inside Out", "note": "Feel your feelings with this Pixar gem."},
        {"title": "The Pursuit of Happyness", "note": "A reminder to keep going."},
        {"title": "Bridge to Terabithia", "note": "Sadness wrapped in wonder."},
        {"title": "The Fault in Our Stars", "note": "Let the tears flow."},
        {"title": "A Silent Voice", "note": "Anime that understands pain."},
        {"title": "Her", "note": "Beautiful loneliness."},
        {"title": "Up", "note": "Adventure is out there — and so is loss."},
        {"title": "Grave of the Fireflies", "note": "A heartbreaking masterpiece."},
        {"title": "Eternal Sunshine of the Spotless Mind", "note": "Melancholy and memory."},
        {"title": "Blue Valentine", "note": "For when love hurts."},
        {"title": "Lion", "note": "Home is a feeling."},
        {"title": "Marley & Me", "note": "A dog's life and goodbye."},
        {"title": "Five Feet Apart", "note": "Distance and closeness."},
        {"title": "All the Bright Places", "note": "Messy, but real."},
        {"title": "A Monster Calls", "note": "Stories help us say goodbye."},
        {"title": "My Girl", "note": "Coming-of-age and letting go."},
        {"title": "Ordinary People", "note": "What grief looks like."},
        {"title": "Pieces of a Woman", "note": "Raw, hard, but honest."},
        {"title": "Wild", "note": "Grief, walking, and healing."},
        {"title": "Silver Linings Playbook", "note": "Love through the storm."}
    ],

    "happy": [
        {"title": "Paddington 2", "note": "The purest bear energy."},
        {"title": "Mamma Mia!", "note": "Sing, dance, and laugh."},
        {"title": "La La Land", "note": "Chase your dreams, in color."},
        {"title": "The Grand Budapest Hotel", "note": "Wes Anderson's pastel perfection."},
        {"title": "Chef", "note": "Cooking + road trip = joy."},
        {"title": "Zootopia", "note": "Believe in yourself."},
        {"title": "The Intouchables", "note": "Friendship heals."},
        {"title": "Sing Street", "note": "Make a band. Change your life."},
        {"title": "School of Rock", "note": "Jack Black energy boost."},
        {"title": "Luca", "note": "A summer you won’t forget."},
        {"title": "Amélie", "note": "Whimsy, Paris, kindness."},
        {"title": "Coco", "note": "Family and music forever."},
        {"title": "Yes Man", "note": "Say yes to life."},
        {"title": "Julie & Julia", "note": "Cooking your way to joy."},
        {"title": "About Time", "note": "Time travel and love."},
        {"title": "Klaus", "note": "The Christmas spirit year-round."},
        {"title": "Ratatouille", "note": "Anyone can cook."},
        {"title": "The Secret Life of Walter Mitty", "note": "Adventure is out there."},
        {"title": "The Hundred-Foot Journey", "note": "Food and family across borders."},
        {"title": "Tangled", "note": "Let your hair down and sing."}
    ],

    "angry": [
        {"title": "Whiplash", "note": "Channel rage into rhythm."},
        {"title": "Fight Club", "note": "Controlled chaos."},
        {"title": "John Wick", "note": "Release that inner hitman."},
        {"title": "Mad Max: Fury Road", "note": "Screaming into the desert."},
        {"title": "The Batman", "note": "Vengeance mode: on."},
        {"title": "Joker", "note": "Madness has a story."},
        {"title": "The Social Network", "note": "Revenge, but make it code."},
        {"title": "The Revenant", "note": "Crawl back, survive, rage."},
        {"title": "Prisoners", "note": "Grief meets fury."},
        {"title": "Oldboy", "note": "Korean vengeance spiral."},
        {"title": "Uncut Gems", "note": "Anxiety-fueled decisions."},
        {"title": "Beast", "note": "Raw emotion in the wild."},
        {"title": "Gone Girl", "note": "Revenge and manipulation."},
        {"title": "Kill Bill", "note": "Tarantino catharsis."},
        {"title": "Gladiator", "note": "Strength and vengeance."},
        {"title": "300", "note": "This is Sparta-level rage."},
        {"title": "The Northman", "note": "Blood and howling."},
        {"title": "Scarface", "note": "Anger meets ambition."},
        {"title": "The Hateful Eight", "note": "Snow and savagery."},
        {"title": "Wrath of Man", "note": "Quiet, calculated fury."}
    ],

    "burntout": [
        {"title": "The Secret Life of Walter Mitty", "note": "Escape into adventure."},
        {"title": "Soul", "note": "Rediscover your spark."},
        {"title": "Julie & Julia", "note": "Find joy in cooking."},
        {"title": "Eat Pray Love", "note": "Travel through the fog."},
        {"title": "Chef", "note": "Reignite your passion."},
        {"title": "Little Miss Sunshine", "note": "Dysfunction can still move forward."},
        {"title": "Dead Poets Society", "note": "Seize the day again."},
        {"title": "Good Will Hunting", "note": "You matter more than your work."},
        {"title": "Amélie", "note": "Kindness is never wasted."},
        {"title": "Begin Again", "note": "Start over with music."},
        {"title": "The Intern", "note": "Age doesn't define you."},
        {"title": "Hector and the Search for Happiness", "note": "What makes life good?"},
        {"title": "Big Fish", "note": "Remember the wonder."},
        {"title": "A Man Called Otto", "note": "Even grumpy hearts need love."},
        {"title": "Lars and the Real Girl", "note": "Strangeness heals."},
        {"title": "Paterson", "note": "Poetry in the mundane."},
        {"title": "Kiki's Delivery Service", "note": "Finding your rhythm again."},
        {"title": "The Way", "note": "Grief and walking as medicine."},
        {"title": "On the Basis of Sex", "note": "Purpose brings power."},
        {"title": "The Hundred-Foot Journey", "note": "Reignite taste and soul."}
    ],

     "anxious": [
        {"title": "My Neighbor Totoro", "note": "A gentle fantasy."},
        {"title": "Finding Nemo", "note": "Just keep swimming."},
        {"title": "A Beautiful Day in the Neighborhood", "note": "Fred Rogers calms the storm."},
        {"title": "Fantastic Mr. Fox", "note": "Chaos made calm."},
        {"title": "The Little Prince", "note": "For the anxious child within."},
        {"title": "Winnie the Pooh", "note": "Soft, slow, kind."},
        {"title": "Big Hero 6", "note": "Support and science."},
        {"title": "Luca", "note": "Feel the summer breeze."},
        {"title": "Inside Out", "note": "Name your emotions."},
        {"title": "The Boy, the Mole, the Fox and the Horse", "note": "Soothing animation for the soul."},
        {"title": "The Peanut Butter Falcon", "note": "Uplifting and quirky."},
        {"title": "The Secret Garden", "note": "Breath in nature."},
        {"title": "The Pursuit of Happyness", "note": "Small steps, big hope."},
        {"title": "Spirited Away", "note": "Lose yourself gently."},
        {"title": "Howl's Moving Castle", "note": "Floating away from worry."},
        {"title": "Paddington", "note": "Cozy joy."},
        {"title": "Song of the Sea", "note": "Myth, grief, calm."},
        {"title": "A Man Called Ove", "note": "Stillness in sadness."},
        {"title": "About Time", "note": "Time to breathe."},
        {"title": "Miss Potter", "note": "Art heals worry."}
    ],

    "inlove": [
        {"title": "Pride and Prejudice", "note": "The original slow-burn."},
        {"title": "Call Me by Your Name", "note": "Sun-drenched longing."},
        {"title": "500 Days of Summer", "note": "Real love and timing."},
        {"title": "Your Name", "note": "Anime romance that wrecks you."},
        {"title": "Titanic", "note": "Iconic, tragic love."},
        {"title": "To All the Boys I've Loved Before", "note": "Modern-day sweetness."},
        {"title": "The Spectacular Now", "note": "Flawed and beautiful."},
        {"title": "A Walk to Remember", "note": "Faith and first love."},
        {"title": "Before Sunrise", "note": "Walking and wondering together."},
        {"title": "Me Before You", "note": "Love in impossible places."},
        {"title": "The Vow", "note": "Love despite memory."},
        {"title": "Notting Hill", "note": "Just a boy, just a girl."},
        {"title": "Letters to Juliet", "note": "Old and new romance."},
        {"title": "La La Land", "note": "Dreamers' romance."},
        {"title": "The Big Sick", "note": "Funny and heartfelt."},
        {"title": "Crazy Rich Asians", "note": "Glitz, heart, and family."},
        {"title": "Midnight in Paris", "note": "Nostalgia + love."},
        {"title": "Always Be My Maybe", "note": "Second chances."},
        {"title": "Palm Springs", "note": "Stuck in time, falling in love."},
        {"title": "Moonrise Kingdom", "note": "Young love in wild places."}
    ],

    "nostalgic": [
        {"title": "Back to the Future", "note": "Timeless classic."},
        {"title": "The Goonies", "note": "Adventure as a kid."},
        {"title": "Stand By Me", "note": "Friendship, loss, and summer."},
        {"title": "The Sandlot", "note": "Baseball and innocence."},
        {"title": "Toy Story", "note": "Growing up hurts."},
        {"title": "E.T. the Extra-Terrestrial", "note": "Phone home, feel again."},
        {"title": "Matilda", "note": "Power to the kind."},
        {"title": "The Iron Giant", "note": "You are who you choose to be."},
        {"title": "The Princess Bride", "note": "Fairy tale perfection."},
        {"title": "Ferris Bueller's Day Off", "note": "Skip school, live life."},
        {"title": "The Karate Kid", "note": "Wax on, nostalgia on."},
        {"title": "Home Alone", "note": "Every 90s kid’s dream."},
        {"title": "Anne of Green Gables", "note": "Imagination and heart."},
        {"title": "The Parent Trap", "note": "Double trouble memories."},
        {"title": "A Christmas Story", "note": "BB guns and snowflakes."},
        {"title": "Bridge to Terabithia", "note": "Painful, magical childhood."},
        {"title": "Hook", "note": "Don’t grow up too fast."},
        {"title": "Little Women (1994 or 2019)", "note": "Sisterhood and time."},
        {"title": "Big", "note": "Be a kid again."},
        {"title": "The Chronicles of Narnia", "note": "Wardrobe to wonderland."}
     ]
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    mood = request.form.get("mood")
    if not mood or mood.lower() not in moods:
        return render_template("recommend.html", movies=[], mood="Unknown", advice="Hmm, I don't recognize that feeling.", color="#888")

    selected_movies = random.sample(moods[mood.lower()], 5)
    advice = random.choice(advice_quotes)
    color = mood_colors.get(mood.lower(), "#444")

    return render_template("recommend.html", movies=selected_movies, mood=mood.title(), advice=advice, color=color)

if __name__ == "__main__":
    app.run(debug=True)
