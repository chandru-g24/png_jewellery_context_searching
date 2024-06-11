import os
from dotenv import load_dotenv
from groq import Groq
import re
import json

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

Prompt = """
Imagine you're developing a system to assist users in finding specific types of jewelry based on their preferences. Your task is to design a JSON structure that takes a user's query as input and extracts relevant information from a predefined dataset of jewelry products. This JSON format should serve as a structured filter option, organizing and presenting relevant data based on the user's query. Ensure that the JSON response includes only relevant information and avoids displaying empty dictionaries for categories without matching items.

The structure should include:
A set of product categories such as "gold," "silver," and "diamond," each containing subcategories like "Earrings," "Rings," "Pendants," and so forth.
For each subcategory, list the available types and styles of jewelry.
Additionally, incorporate filter options such as price range, occasion, and gender to further refine the search results. And use the given example queries and outputs to validate your JSON structure, ensuring it correctly maps user queries to relevant product information while considering filters like price, occasion, and gender.
If the user asking to suggest and list the models show the available all models in corresponding products.
{
    "products": {
        "gold": {
            "Earrings": {
                "types": ["daily", "office", "party"],
                "styles": ["studs", "jumkhas", "dropsand danglers", "hoops and huggies", "men studs"]
            },
            "Rings": {
                "types": ["daily", "office", "party"],
                "styles": ["causal", "fashion", "couple", "traditional"]
            },
            "Pendant": {
                "styles": ["charm", "heart", "religious", "classic", "kids"]
            },
            "Necklaces": {
                "types": ["daily", "office", "party"],
                "styles": ["long", "necklace set", "chocker", "thushi", "short necklace"]
            },
            "Bracelets and Bangles": {
                "types": ["daily", "office", "party"],
                "styles": ["Kids Bracelets", "Flexible Bracelets", "Mangalsutra Bracelets", "Oval Bracelets", "Charm Bracelets", "Rakhi", "Gold Bangles"]
            },
            "Mangalsutra": {
                "types": ["daily", "office", "party"],
                "styles": ["Modern Mangalsutra", "Traditional Mangalsutra", "Wati Mani Mangalsutra"]
            },
            "Gold Cufflinks": {
                "styles": ["cufflink"]
            },
            "Gold Chain": {
                "styles": ["Chain"]
            },
            "Gold Nath": {
                "styles": ["nath"]
            },
            "Gold Coin": {
                "styles": ["plain", "PNG", "Laxmi shree"]
            },
            "Gold Vedhani": {
                "styles": ["vedhani"]
            }
        },
        "silver": {
            "Silver Painjan": {
                "styles": ["silver painjan"]
            },
            "Silver Rakhi": {
                "styles": ["silver Rakhi"]
            },
            "Silver Coins": {
                "styles": ["Pure Silver Chip", "Trimurti Silver Coins", "Ganesh Silver Coins", "Laxmi Silver Coin"]
            }
        },
        "diamond": {
            "Earrings": {
                "types": ["daily", "office", "party"],
                "styles": ["studs", "dropsand danglers", "hoops and huggies", "men studs"]
            },
            "Rings": {
                "types": ["daily", "office", "party"],
                "styles": ["causal", "band", "engagement", "fashion", "men", "eternity"]
            },
            "Pendant": {
                "styles": ["charm", "heart", "religious", "classic", "kids", "Zodiac"]
            },
            "Necklaces": {
                "types": ["daily", "office", "party"],
                "styles": ["long", "necklace set", "modern necklaces", "lariat", "short necklace"]
            },
            "Bracelets and Bangles": {
                "types": ["daily", "office", "party"],
                "styles": ["Kids Bracelets", "Flexible Bracelets", "Mangalsutra Bracelets", "Oval Bracelets", "Charm Bracelets", "Rakhi", "Gold Bangles"]
            },
            "Mangalsutra": {
                "types": ["daily", "office", "party"],
                "styles": ["Trendy Modern Mangalsutra", "tanmaniya"]
            },
            "Cufflinks": {
                "styles": ["cufflink"]
            },
            "Nosepin": {
                "styles": ["Nosepin"]
            }
        }
    },
    "filters": {
        "price": [
            "Less than ₹15,000",
            "₹15,001 - ₹20,000",
            "₹20,001 - ₹30,000",
            "₹30,001 - ₹40,000",
            "₹40,001 - ₹50,000",
            "₹50,001 - ₹1,00,000",
            "₹1,00,001 - ₹1,50,000",
            "₹1,50,001 - ₹2,00,000",
            "₹2,00,001 - ₹2,50,000",
            "₹2,50,001 and Above"
        ],
        "occasion": ["Daily Wear", "Officewear", "Party Wear"],
        "gender": ["male", "female", "kids"]
    }
}

Example Queries and Outputs:

Query: "show gold earrings less than 10000"
Output:
{
  "gold": {
    "Earrings": {
      "types": ["daily", "office", "party"],
      "styles": ["studs", "jhumkas", "drops and danglers", "hoops and huggies", "men's studs"]
    }
  },
  "filters": {
    "price": ["Less than ₹15,000"],
    "occasion": ["Daily Wear", "Officewear", "Party Wear"],
    "gender": ["male", "female", "kids"]
  }
}

Query: "show diamond rings for men"
Output:
{
  "diamond": {
    "Rings": {
      "types": ["daily", "office", "party"],
      "styles": ["casual", "band", "engagement", "fashion", "men", "eternity"]
    }
  },
  "filters": {
    "occasion": ["Daily Wear", "Office Wear", "Party Wear"],
    "gender": ["male"]
  }
}

Query: "show silver coins"
Output:
{
  "silver": {
    "Silver Coins": {
      "styles": ["Pure Silver Chip", "Trimurti Silver Coins", "Ganesh Silver Coins", "Laxmi Silver Coin"]
    }
  },
  "filters": {
    "occasion": ["Daily Wear", "Office Wear", "Party Wear"],
    "gender": ["male", "female", "kids"]
  }
}

Query: "show gold necklaces for office wear"
Output:
{
  "gold": {
    "Necklaces": {
      "types": ["daily", "office", "party"],
      "styles": ["long", "necklace set", "choker", "thushi", "short necklace"]
    }
  },
  "filters": {
    "occasion": ["Office Wear"],
    "gender": ["male", "female", "kids"]
  }
}

Query: "show diamond pendants for kids"
Output:
{
  "diamond": {
    "Pendant": {
      "styles": ["charm", "heart", "religious", "classic", "kids", "zodiac"]
    }
  },
  "filters": {
    "occasion": ["Daily Wear", "Office Wear", "Party Wear"],
    "gender": ["kids"]
  }
}

Query: "show men stud"
Output:

{
  "gold": {
    "Earrings": {
      "types": ["daily", "office", "party"],
      "styles": ["men's studs"]
    }
  },
  "diamond": {
    "Earrings": {
      "types": ["daily", "office", "party"],
      "styles": ["men's studs"]
    }
  },
  "filters": {
    "occasion": ["Daily Wear", "Office Wear", "Party Wear"],
    "gender": ["male"]
  }
}

Query: "show religious pendant below 50000"
Output:
{
  "gold": {
    "Pendant": {
      "styles": ["religious"]
    }
  },
  "diamond": {
    "Pendant": {
      "styles": ["religious"]
    }
  },
  "filters": {
    "price": ["₹40,001 - ₹50,000"],
    "occasion": ["Daily Wear", "Office Wear", "Party Wear"],
    "gender": ["male", "female", "kids"]
  }
}

Query:"suggest me some diamond necklaces"
Output:
{
  "diamond":{
    "Necklaces":{
        "types": ["daily", "office", "party"],
        "styles": ["long", "necklace set", "modern necklaces", "lariat", "short necklace"]
    }
  }
  "filters": {
    "price": [
        "Less than ₹15,000",
        "₹15,001 - ₹20,000",
        "₹20,001 - ₹30,000",
        "₹30,001 - ₹40,000",
        "₹40,001 - ₹50,000",
        "₹50,001 - ₹1,00,000",
        "₹1,00,001 - ₹1,50,000",
        "₹1,50,001 - ₹2,00,000",
        "₹2,00,001 - ₹2,50,000",
        "₹2,50,001 and Above"
    ],
    "occasion": ["Daily Wear", "Officewear", "Party Wear"],
    "gender": ["male", "female", "kids"]
    }
  }
}
Query:"I want the gold earings and silver rings and diamond jumkhas for office"
Output:
{
    "gold": {
        "Earrings": {
            "types": [
                "office"
            ],
            "styles": [
                "studs",
                "jhumkas",
                "drops and danglers",
                "hoops and huggies",
                "men studs"
            ]
        }
    },
    "silver": {
        "Rings": {
            "types": [
                "office"
            ],
            "styles": [
                "silver Rakhi",
                "silver Painjan"
            ]
        }
    },
    "diamond": {
        "Earrings": {
            "types": [
                "office"
            ],
        }
    },
    "filters": {
        "occasion": [
            "Office Wear"
        ],
        "gender": [
            "male",
            "female",
            "kids"
        ]
    }
}
"""


def extract_json_from_string(s):
    # Regular expression to match the JSON part of the string
    json_pattern = re.compile(r'\{.*\}', re.DOTALL)

    # Search for the JSON pattern in the string
    match = json_pattern.search(s)

    if match:
        json_str = match.group(0)
        return json_str
    else:
        return None


def input_utterance(input):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": Prompt,
            },
            {
                "role": "user",
                "content": input}],
        model="llama3-70b-8192",
    )

    response = chat_completion.choices[0].message.content
    response = extract_json_from_string(response)
    response = json.loads(response)
    return response


if __name__ == "__main__":
    input_utterance(input="list me a office studs for men under 12000")
