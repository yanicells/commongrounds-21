from merchstore.models import Product
from localevents.models import Event
from bookclub.models import Book
from diyprojects.models import Project
from commissions.models import Commission
from grounds.models import Post

def get_all_context():
    context = [
        "You are the Common Grounds AI Assistant. Your goal is to help users navigate and understand the Common Grounds platform.",
        "Below is the current state of the database including products, books, events, projects, commissions, and community posts.",
        "Use this information to answer user questions accurately. If you don't know the answer, say you don't know. Also, you are restricted to only answering and assisting with regards to the Common Grounds platform. Do not respond to any other queries.",
        "Do not use markdown. Just do plain text. Don't indent.",
        "About the team/developers of common grounds. Edrian Capistrano, John Kyrk Terrobias, Sofia Dion Torres, Nathan Martin, and Edizon Infante.",
        "\n--- Platform Modules ---",
        "MerchStore: A marketplace for users to buy and sell products. Users can browse listings and manage their own inventory.",
        "Book Club: A community library for sharing books. Users can contribute books to the collection or borrow available ones.",
        "Local Events: A place for organizing community gatherings. Users can sign up for events and track attendee capacity.",
        "DIY Projects: A space for creators to showcase guides and projects. Users can explore creative builds and find inspiration.",
        "Commissions: A platform for custom work. Users can create commission requests or fulfill jobs as a maker.",
        "Grounds: A community freedom wall for members to share updates, thoughts, and images. Anyone logged in can contribute.",
        "\n--- Merchandise Store Products ---"
    ]

    products = Product.objects.all()
    for p in products:
        context.append(f"Product: {p.name} | Price: {p.price} | Stock: {p.stock} | Status: {p.status} | Owner: {p.owner.display_name}")
    
    books = Book.objects.all()
    context.append("\n--- Book Club Collection ---")
    for b in books:
        status = "Available" if b.available_to_borrow else "Borrowed"
        genre_name = b.genre.name if b.genre else "General"
        context.append(f"Book: {b.title} by {b.author} | Genre: {genre_name} | Status: {status} | Contributed by: {b.contributor.display_name if b.contributor else 'Anonymous'}")

    events = Event.objects.all()
    context.append("\n--- Local Events ---")
    for e in events:
        organizer = e.organizer.first().display_name if e.organizer.exists() else "Unknown"
        context.append(f"Event: {e.title} | Location: {e.location} | Status: {e.get_status_display()} | Organizer: {organizer} | Capacity: {e.event_capacity}")

    projects = Project.objects.all()
    context.append("\n--- DIY Projects ---")
    for pr in projects:
        context.append(f"Project: {pr.title} | Category: {pr.category.name if pr.category else 'General'} | Creator: {pr.creator.display_name if pr.creator else 'Anonymous'}")

    commissions = Commission.objects.all()
    context.append("\n--- Commission Requests ---")
    for c in commissions:
        context.append(f"Commission: {c.title} | Type: {c.commission_type} | Status: {c.get_status_display()} | Maker: {c.maker.display_name}")

    posts = Post.objects.all()[:10]
    context.append("\n--- Latest from the Grounds ---")
    for po in posts:
        author_name = po.author.display_name or po.author.user.username
        context.append(f"Post by {author_name}: {po.title} - {po.description[:50]}...")

    return "\n".join(context)
