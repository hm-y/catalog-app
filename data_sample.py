# Import & Set up the session

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Base, Category, Item, User

engine = create_engine('sqlite:///content.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Apply Sample data

# The user: Admin

admin = User(name="Admin", email="admin@admin.com")

# Category 1 and its items

cat1 = Category(name="Books", user=admin)

session.add(cat1)
session.commit()

item1 = Item(title="The Republic",
                     description="Not only is it an important piece of work from one of the most influential philosophers, \
                     it's also very readable.",
                     category=cat1, user=admin)
session.add(item1)
session.commit()

item2 = Item(title="The Wealth of Nations",
                     description="Smith's book has been described as --the foundation of economics, \
                     the origin of econometrics and the intellectual cradle of capitalism--, \
                     all of which are as relevant today as they were when he wrote it.",
                     category=cat1, user=admin)
session.add(item2)
session.commit()

item3 = Item(title="Nineteen Eighty-Four",
                     description="--It's much more than a book - it's a novel of huge social and political \
                     significance that's never going to date,-- says Abe Books, \
                     especially in an age of digital surveillance. \
                     Is Big Brother watching you?",
                     category=cat1, user=admin)
session.add(item3)
session.commit()

item4 = Item(title="A Brief History of Time",
                     description="It tackles one of the biggest and most intriguing questions: \
                     where did we come from and where are we going?",
                     category=cat1, user=admin)
session.add(item4)
session.commit()

item5 = Item(title="The Prince",
                     description="The Prince provided aspiring rulers \
                     with a guide on getting power and holding on to it.",
                     category=cat1, user=admin)
session.add(item5)
session.commit()

# Category 2 and its items

cat2 = Category(name="Movies", user=admin)

session.add(cat2)
session.commit()

item1 = Item(title="The Dark Knight",
                     description="When the menace known as the Joker emerges from his mysterious past, \
                     he wreaks havoc and chaos on the people of Gotham, the Dark Knight must accept \
                     one of the greatest psychological and physical tests of his ability to fight injustice.",
                     category=cat2, user=admin)
session.add(item1)
session.commit()

item2 = Item(title="12 Angry Men",
                     description="A jury holdout attempts to prevent a miscarriage of \
                     justice by forcing his colleagues to reconsider the evidence.",
                     category=cat2, user=admin)
session.add(item2)
session.commit()

item3 = Item(title="Pulp Fiction",
                     description="The lives of two mob hit men, a boxer, a gangster's wife, \
                     and a pair of diner bandits intertwine in four tales of violence and redemption.",
                     category=cat2, user=admin)
session.add(item3)
session.commit()


item4 = Item(title="The Matrix",
                     description="A computer hacker learns from mysterious rebels \
                     about the true nature of his reality and his role in the war against its controllers.",
                     category=cat2, user=admin)
session.add(item4)
session.commit()


item5 = Item(title="Seven Samurai",
                     description="A poor village under attack by bandits recruits \
                     seven unemployed samurai to help them defend themselves.",
                     category=cat2, user=admin)
session.add(item5)
session.commit()

# Category 3 and its items

cat3 = Category(name="Musics", user=admin)

session.add(cat3)
session.commit()


item1 = Item(title="A Change Is Gonna Come",
                     description="Cooke wrote this protest song to support \
                     the civil rights movement in the United States. ",
                     category=cat3, user=admin)
session.add(item1)
session.commit()

item2 = Item(title="I Wanna Hold Your Hand",
                     description="This song supposedly kickstarted \
                     the glorious music revolution of the 1960s.",
                     category=cat3, user=admin)
session.add(item2)
session.commit()

item3 = Item(title="Strange Fruit",
                     description="Billie Holiday's Strange Fruit is \
                     a protest song with enduring relevance.",
                     category=cat3, user=admin)
session.add(item3)
session.commit()


item4 = Item(title="Imagine",
                     description="Widely regarded as John Lennon's signature song, \
                     Imagine was the title track of his second album, \
                     and is perhaps his best-known solo work. ",
                     category=cat3, user=admin)
session.add(item4)
session.commit()


item5 = Item(title="Sunday Bloody Sunday",
                     description="One of U2's most overtly political songs",
                     category=cat3, user=admin)
session.add(item5)
session.commit()

# Category 4 and its items

cat4 = Category(name="Foods", user=admin)

session.add(cat4)
session.commit()



item1 = Item(title="Buttered popcorn",
                     description="Corn is best when its sweet variety is fried up with lashings of butter \
                     till it bursts and then snarfed in greasy fistfuls while watching Netflix late at night.",
                     category=cat4, user=admin)
session.add(item1)
session.commit()

item2 = Item(title="Tacos",
                     description="This is the reason no visitor leaves Mexico weighing \
                     less than when they arrived.",
                     category=cat4, user=admin)
session.add(item2)
session.commit()

item3 = Item(title="Lasagna",
                     description="Second only to pizza in the list of famed Italian foods, \
                     there's a reason this pasta-layered, tomato-sauce-infused, minced-meaty gift \
                     to kids and adults alike is so popular -- it just works.",
                     category=cat4, user=admin)
session.add(item3)
session.commit()


item4 = Item(title="Croissant",
                     description="Flaky pastry smothered in butter, a pile of raspberry jam smeared \
                     over the top and a soft, giving bite as you sink in your teeth; \
                     there's nothing not to love about this fatty, \
                     sweet breakfast food that must be married to a cup of strong coffee.",
                     category=cat4, user=admin)
session.add(item4)
session.commit()


item5 = Item(title="Peking duck",
                     description="The maltose-syrup glaze coating the skin is the secret. \
                     Slow roasted in an oven, the crispy, syrup-coated skin is so good that \
                     authentic eateries will serve more skin than meat, and bring it with pancakes, \
                     onions and hoisin or sweet bean sauce.",
                     category=cat4, user=admin)
session.add(item5)
session.commit()

# Category 5 and its items

cat5 = Category(name="Websites", user=admin)

session.add(cat5)
session.commit()


item1 = Item(title="Google",
                     description="Google LLC is an American multinational technology company \
                     that specializes in Internet-related services and products.",
                     category=cat5, user=admin)
session.add(item1)
session.commit()

item2 = Item(title="YouTube",
                     description="YouTube is an American video-sharing website \
                     headquartered in San Bruno, California.",
                     category=cat5, user=admin)
session.add(item2)
session.commit()

item3 = Item(title="Facebook",
                     description="Facebook is an American for-profit corporation \
                     and an online social media and social networking service based \
                     in Menlo Park, California.",
                     category=cat5, user=admin)
session.add(item3)
session.commit()


item4 = Item(title="Baidu",
                     description="Baidu, Inc., incorporated on 18 January 2000, \
                     is a Chinese web services company headquartered \
                     at the Baidu Campus in Beijing's Haidian District.",
                     category=cat5, user=admin)
session.add(item4)
session.commit()


item5 = Item(title="Wikipedia",
                     description="Wikipedia is a free online encyclopedia \
                     with the aim to allow anyone to edit articles.",
                     category=cat5, user=admin)
session.add(item5)
session.commit()

# Notify the success!

print "Data sample applied."
