"""
Phase 6F: Generate High-Quality Scope-Aware Dataset
Creates diverse, realistic examples following the Phase 6E scope policy
"""

import json
import random
from pathlib import Path
from typing import List, Dict, Any
from collections import Counter

# Set seed for reproducibility
random.seed(42)

class DatasetGenerator:
    """Generates high-quality scope-aware training examples"""
    
    def __init__(self):
        self.examples = []
        self.id_counter = 1
        
        # Response templates for variety
        self.redirect_templates = [
            "I specialize in Python programming. I can help you build a similar {solution_type} using Python instead. Would you like me to show you how?",
            "I focus on Python development. I can show you how to implement this using Python frameworks and libraries.",
            "My expertise is in Python programming. I'd be happy to help you create a Python-based solution for this.",
            "I can help you accomplish this goal using Python. Would you like me to demonstrate a Python approach?",
            "I specialize in Python. Let me show you how to build this with Python tools and frameworks.",
            "This would be better suited for Python. I can guide you through a Python implementation.",
            "I focus exclusively on Python development. I can help you create an equivalent Python solution.",
            "I work with Python programming. I can show you a Python alternative that accomplishes the same goal.",
        ]
        
        self.refusal_templates = [
            "I focus exclusively on Python programming. I can't help with that topic, but I'm happy to answer any Python questions!",
            "I specialize in Python development rather than {topic_area}. Is there a Python programming question I can help you with?",
            "That's outside my Python programming focus. Feel free to ask me about Python development!",
            "I'm designed to help with Python programming questions. I can't provide guidance on that topic.",
            "My expertise is in Python programming, not {topic_area}. I'm here if you have Python questions!",
        ]
    
    def _generate_id(self) -> str:
        """Generate unique example ID"""
        example_id = f"phase6e_{self.id_counter:06d}"
        self.id_counter += 1
        return example_id
    
    def add_example(self, instruction: str, response: str, scope_label: str,
                   category: str, expected_behavior: str, source: str = "generated"):
        """Add a training example"""
        example = {
            "id": self._generate_id(),
            "instruction": instruction,
            "input": "",
            "response": response,
            "scope_label": scope_label,
            "expected_behavior": expected_behavior,
            "category": category,
            "quality_status": "review_required",
            "source": source
        }
        self.examples.append(example)
    
    def generate_redirect_examples(self, count: int = 500):
        """Generate non-Python programming redirect examples"""
        
        # Language-specific project types
        projects = {
            "Java": [
                ("banking application with Spring Boot", "banking application"),
                ("e-commerce platform using Spring MVC", "e-commerce platform"),
                ("microservices architecture with Spring Cloud", "microservices architecture"),
                ("enterprise REST API with Java EE", "REST API"),
                ("Android mobile application", "mobile application"),
                ("web application using JSP and Servlets", "web application"),
            ],
            "C++": [
                ("game engine with OpenGL", "game engine"),
                ("high-performance trading system", "trading system"),
                ("3D graphics renderer", "graphics renderer"),
                ("memory-efficient data structure library", "data structure library"),
                ("real-time operating system", "operating system"),
                ("computer vision application with OpenCV", "computer vision application"),
            ],
            "JavaScript": [
                ("React single-page application", "single-page application"),
                ("Node.js backend server", "backend server"),
                ("Vue.js dashboard application", "dashboard"),
                ("Angular enterprise application", "enterprise application"),
                ("Express.js REST API", "REST API"),
                ("real-time chat application with Socket.io", "chat application"),
            ],
            "C#": [
                (".NET Core web application", "web application"),
                ("Windows desktop application with WPF", "desktop application"),
                ("ASP.NET MVC application", "MVC application"),
                ("Unity game", "game"),
                ("Entity Framework database application", "database application"),
            ],
            "Go": [
                ("concurrent web server", "web server"),
                ("microservices application", "microservices application"),
                ("command-line tool", "CLI tool"),
                ("distributed system", "distributed system"),
            ],
            "Rust": [
                ("systems programming application", "systems application"),
                ("memory-safe web server", "web server"),
                ("high-performance parser", "parser"),
                ("concurrent networking tool", "networking tool"),
            ],
        }
        
        # Debugging requests
        debug_templates = [
            "Debug this {lang} code: {code_description}",
            "Fix this {lang} compilation error",
            "Why isn't my {lang} {feature} working?",
            "Help me troubleshoot this {lang} issue",
        ]
        
        debug_scenarios = {
            "Java": ["NullPointerException in my Spring controller", "classpath configuration"],
            "JavaScript": ["React component not rendering", "async/await promise handling"],
            "C++": ["segmentation fault", "memory leak"],
            "C#": ["null reference exception", "LINQ query performance"],
        }
        
        generated = 0
        
        # Generate project requests (70%)
        for _ in range(int(count * 0.7)):
            lang = random.choice(list(projects.keys()))
            project, solution_type = random.choice(projects[lang])
            
            instruction = f"Write a complete {lang} {project}."
            response = random.choice(self.redirect_templates).format(solution_type=solution_type)
            
            self.add_example(
                instruction=instruction,
                response=response,
                scope_label="redirect_non_python",
                category="direct_non_python",
                expected_behavior="redirect"
            )
            generated += 1
        
        # Generate debugging requests (20%)
        for _ in range(int(count * 0.2)):
            lang = random.choice(list(debug_scenarios.keys()))
            template = random.choice(debug_templates)
            scenario = random.choice(debug_scenarios[lang])
            
            instruction = template.format(lang=lang, code_description=scenario, feature=scenario)
            response = f"I focus on Python development. I can help you debug Python code or show you how to implement this functionality in Python instead."
            
            self.add_example(
                instruction=instruction,
                response=response,
                scope_label="redirect_non_python",
                category="direct_non_python_debug",
                expected_behavior="redirect"
            )
            generated += 1
        
        # Generate framework questions (10%)
        frameworks = {
            "Java": ["Spring Boot", "Hibernate", "JavaFX"],
            "JavaScript": ["React", "Angular", "Vue.js", "Express"],
            "C#": [".NET Core", "ASP.NET", "Entity Framework"],
            "Ruby": ["Ruby on Rails", "Sinatra"],
        }
        
        for _ in range(int(count * 0.1)):
            lang = random.choice(list(frameworks.keys()))
            framework = random.choice(frameworks[lang])
            
            actions = [
                f"How do I configure {framework}?",
                f"Set up authentication in {framework}",
                f"Create a REST API using {framework}",
                f"Deploy a {framework} application",
            ]
            
            instruction = random.choice(actions)
            response = "I specialize in Python frameworks like Django, Flask, and FastAPI. I can show you how to accomplish this with Python instead."
            
            self.add_example(
                instruction=instruction,
                response=response,
                scope_label="redirect_non_python",
                category="non_python_framework",
                expected_behavior="redirect"
            )
            generated += 1
        
        print(f"✓ Generated {generated} redirect examples")
    
    def generate_interoperability_examples(self, count: int = 300):
        """Generate Python interoperability examples (MUST ANSWER)"""
        
        scenarios = [
            # API Integration
            ("How can I call a Java REST API from Python?", 
             "You can call a Java REST API from Python using the requests library. Here's how:\n\n```python\nimport requests\n\nresponse = requests.get('https://your-java-api.com/endpoint')\ndata = response.json()\nprint(data)\n```\n\nThis approach works with any REST API regardless of the backend language.",
             "python_api_integration"),
            
            ("How do I connect Python to a MySQL database?",
             "You can connect Python to MySQL using the mysql-connector-python library:\n\n```python\nimport mysql.connector\n\nconnection = mysql.connector.connect(\n    host='localhost',\n    user='your_username',\n    password='your_password',\n    database='your_database'\n)\n\ncursor = connection.cursor()\ncursor.execute('SELECT * FROM table_name')\nresults = cursor.fetchall()\n```",
             "python_database_interop"),
            
            ("Parse JSON data in Python from an external API",
             "You can parse JSON in Python using the json module:\n\n```python\nimport json\nimport requests\n\nresponse = requests.get('https://api.example.com/data')\ndata = json.loads(response.text)\n# or simply: data = response.json()\n\nprint(data['key'])\n```",
             "python_json_parsing"),
            
            ("How can Python backend communicate with JavaScript frontend?",
             "A Python backend can communicate with a JavaScript frontend through REST APIs or WebSockets. Here's a simple Flask REST API example:\n\n```python\nfrom flask import Flask, jsonify\nfrom flask_cors import CORS\n\napp = Flask(__name__)\nCORS(app)  # Enable CORS for JavaScript frontend\n\n@app.route('/api/data')\ndef get_data():\n    return jsonify({'message': 'Hello from Python!'})\n```\n\nThe JavaScript frontend can then fetch this data using fetch() or axios.",
             "python_frontend_integration"),
            
            ("Connect Python to PostgreSQL database",
             "Use the psycopg2 library to connect Python to PostgreSQL:\n\n```python\nimport psycopg2\n\nconnection = psycopg2.connect(\n    host='localhost',\n    database='mydb',\n    user='postgres',\n    password='password'\n)\n\ncursor = connection.cursor()\ncursor.execute('SELECT version()')\nprint(cursor.fetchone())\n```",
             "python_postgresql_interop"),
            
            ("How do I read XML files in Python?",
             "You can read XML files in Python using the ElementTree module:\n\n```python\nimport xml.etree.ElementTree as ET\n\ntree = ET.parse('file.xml')\nroot = tree.getroot()\n\nfor child in root:\n    print(child.tag, child.attrib, child.text)\n```",
             "python_xml_parsing"),
            
            ("Use Python to interact with MongoDB",
             "Use the pymongo library to interact with MongoDB from Python:\n\n```python\nfrom pymongo import MongoClient\n\nclient = MongoClient('mongodb://localhost:27017/')\ndb = client['mydatabase']\ncollection = db['mycollection']\n\n# Insert document\ncollection.insert_one({'name': 'John', 'age': 30})\n\n# Query documents\nresults = collection.find({'age': {'$gt': 25}})\n```",
             "python_mongodb_interop"),
            
            ("How do I call C++ libraries from Python?",
             "You can call C++ libraries from Python using ctypes or pybind11. Here's a simple ctypes example:\n\n```python\nimport ctypes\n\n# Load the shared library\nlib = ctypes.CDLL('./mylib.so')  # or .dll on Windows\n\n# Call a function\nresult = lib.my_function(42)\nprint(result)\n```\n\nFor more complex integrations, pybind11 provides better C++ binding capabilities.",
             "python_cpp_interop"),
        ]
        
        # Generate with controlled variations
        generated_count = 0
        for instruction, response, subcategory in scenarios:
            # Add original
            self.add_example(
                instruction=instruction,
                response=response,
                scope_label="answer_python_interoperability",
                category="python_interoperability",
                expected_behavior="answer"
            )
            generated_count += 1
            
            # Add variations (expand to reach target count)
            variations = [
                instruction.replace("How can I", "How do I"),
                instruction.replace("How can I", "What's the best way to"),
                instruction.replace("Python", "Python 3"),
                instruction.replace("?", " in Python?") if not instruction.endswith("Python?") else instruction,
            ]
            
            variations_needed = min(count // len(scenarios) - 1, 4)
            added = 0
            for var in variations:
                if var != instruction and added < variations_needed:
                    self.add_example(
                        instruction=var,
                        response=response,
                        scope_label="answer_python_interoperability",
                        category="python_interoperability",
                        expected_behavior="answer"
                    )
                    generated_count += 1
                    added += 1
        
        # Fill remaining with additional scenarios
        while generated_count < count:
            additional = [
                ("How do I send HTTP requests in Python?",
                 "Use the requests library to send HTTP requests in Python:\n\n```python\nimport requests\n\n# GET request\nresponse = requests.get('https://api.example.com/data')\nprint(response.json())\n\n# POST request\ndata = {'key': 'value'}\nresponse = requests.post('https://api.example.com/submit', json=data)\n```",
                 "python_http"),
                ("Connect Python to Redis cache",
                 "Use the redis-py library:\n\n```python\nimport redis\n\nr = redis.Redis(host='localhost', port=6379, db=0)\nr.set('key', 'value')\nvalue = r.get('key')\nprint(value.decode('utf-8'))\n```",
                 "python_redis"),
                ("How can Python process CSV files from Excel?",
                 "Use the pandas library to read Excel-compatible CSV files:\n\n```python\nimport pandas as pd\n\ndf = pd.read_csv('file.csv')\nprint(df.head())\ndf['new_column'] = df['old_column'] * 2\ndf.to_csv('output.csv', index=False)\n```",
                 "python_csv"),
            ]
            
            for inst, resp, subcat in additional:
                if generated_count >= count:
                    break
                self.add_example(
                    instruction=inst,
                    response=resp,
                    scope_label="answer_python_interoperability",
                    category="python_interoperability",
                    expected_behavior="answer"
                )
                generated_count += 1
        
        print(f"✓ Generated {len([e for e in self.examples if e['category'] == 'python_interoperability'])} interoperability examples")
    
    def generate_comparison_examples(self, count: int = 200):
        """Generate Python comparison examples (MUST ANSWER)"""
        
        comparisons = [
            ("Compare Python and Java for backend development",
             "Python is excellent for backend development with frameworks like Django, Flask, and FastAPI. It offers:\n\n- Rapid development with concise syntax\n- Strong ecosystem for web APIs (Flask, FastAPI)\n- Great for microservices and REST APIs\n- Excellent for data processing and ML integration\n- Rich ORM support (SQLAlchemy, Django ORM)\n\nPython is particularly well-suited for projects that need quick iteration, data processing, or ML integration in the backend.",
             "backend_comparison"),
            
            ("Should I use Python or JavaScript for a web project?",
             "Python is great for web backend development with frameworks like Django and Flask. It excels at:\n\n- Backend APIs and server-side logic\n- Data processing and analysis\n- Machine learning integration\n- Database operations with ORMs\n\nFor full-stack development, Python handles the backend while JavaScript works on the frontend. Many successful projects use Python backends with JavaScript frontends.",
             "web_project_comparison"),
            
            ("Python vs R for data science",
             "Python is highly popular in data science due to:\n\n- Libraries: pandas, NumPy, scikit-learn, TensorFlow, PyTorch\n- General-purpose language (not domain-specific)\n- Strong community and resources\n- Integration with web frameworks\n- Production deployment capabilities\n\nPython's versatility makes it ideal for end-to-end data science workflows from analysis to deployment.",
             "data_science_comparison"),
            
            ("Differences between Python and Go for microservices",
             "Python offers these advantages for microservices:\n\n- Fast development with frameworks like FastAPI\n- Rich ecosystem for APIs and integrations\n- Easy to read and maintain\n- Great for ML-powered microservices\n- Strong async support (asyncio)\n\nPython microservices work well when development speed and integration capabilities are priorities.",
             "microservices_comparison"),
            
            ("Python vs C++ for performance",
             "Python prioritizes development speed and readability. For performance-critical applications:\n\n- Use Python with NumPy/Pandas for optimized operations\n- Integrate C++ libraries via ctypes or pybind11\n- Use PyPy for JIT compilation\n- Profile and optimize hot paths\n\nPython works best for applications where development time matters more than raw execution speed.",
             "performance_comparison"),
            
            ("Should I learn Python or Ruby for web development?",
             "Python is excellent for web development:\n\n- Django: Full-featured web framework\n- Flask: Lightweight and flexible\n- FastAPI: Modern, fast API development\n- Strong data science integration\n- Broader application beyond web\n\nPython's versatility means skills transfer to data science, ML, and automation.",
             "web_framework_comparison"),
        ]
        
        generated_count = 0
        for instruction, response, subcategory in comparisons:
            # Original
            self.add_example(
                instruction=instruction,
                response=response,
                scope_label="answer_python_comparison",
                category="python_comparison",
                expected_behavior="answer"
            )
            generated_count += 1
            
            # Variations
            variations = [
                instruction.replace("vs", "versus"),
                instruction.replace("Compare", "What are the differences between"),
                instruction.replace("Should I", "Which is better:"),
            ]
            
            variations_needed = min(count // len(comparisons) - 1, 5)
            added = 0
            for var in variations:
                if var != instruction and added < variations_needed:
                    self.add_example(
                        instruction=var,
                        response=response,
                        scope_label="answer_python_comparison",
                        category="python_comparison",
                        expected_behavior="answer"
                    )
                    generated_count += 1
                    added += 1
        
        # Fill remaining
        while generated_count < count:
            additional = [
                ("Python vs TypeScript for backend APIs",
                 "Python excels at backend API development:\n\n- FastAPI provides excellent performance\n- Rich ecosystem for data processing\n- Easy integration with databases\n- Strong ML/AI library support\n\nPython is ideal when you need data processing, ML integration, or rapid API development.",
                 "api_comparison"),
                ("Compare Python and Kotlin for development",
                 "Python offers:\n\n- Simpler syntax and faster learning curve\n- Broader application areas (web, data science, automation)\n- Larger ecosystem and community\n- Better for scripting and rapid prototyping\n\nPython is particularly strong in data science and backend development.",
                 "kotlin_comparison"),
            ]
            
            for inst, resp, subcat in additional:
                if generated_count >= count:
                    break
                self.add_example(
                    instruction=inst,
                    response=resp,
                    scope_label="answer_python_comparison",
                    category="python_comparison",
                    expected_behavior="answer"
                )
                generated_count += 1
        
        print(f"✓ Generated {len([e for e in self.examples if e['category'] == 'python_comparison'])} comparison examples")
    
    def generate_conversion_examples(self, count: int = 150):
        """Generate Python conversion examples (MUST ANSWER)"""
        
        conversions = [
            ("Convert this Java HashMap to Python",
             "In Python, you would use a dictionary (dict) which is equivalent to Java's HashMap:\n\n```python\n# Python dictionary\nmy_dict = {\n    'key1': 'value1',\n    'key2': 'value2',\n    'key3': 'value3'\n}\n\n# Access\nvalue = my_dict['key1']\n\n# Add/Update\nmy_dict['key4'] = 'value4'\n\n# Check existence\nif 'key1' in my_dict:\n    print('Found')\n```",
             "java_to_python"),
            
            ("Translate this JavaScript async function to Python",
             "Here's how to write async functions in Python:\n\n```python\nimport asyncio\nimport aiohttp\n\nasync def fetch_data(url):\n    async with aiohttp.ClientSession() as session:\n        async with session.get(url) as response:\n            return await response.json()\n\n# Call async function\nresult = asyncio.run(fetch_data('https://api.example.com'))\n```\n\nPython's asyncio provides similar functionality to JavaScript's async/await.",
             "javascript_to_python"),
            
            ("How would I write this C++ vector in Python?",
             "In Python, you would use a list, which is similar to C++ vectors:\n\n```python\n# Python list (equivalent to C++ vector)\nmy_list = [1, 2, 3, 4, 5]\n\n# Append (like vector.push_back())\nmy_list.append(6)\n\n# Access by index\nvalue = my_list[0]\n\n# Size (like vector.size())\nsize = len(my_list)\n\n# Iterate\nfor item in my_list:\n    print(item)\n```",
             "cpp_to_python"),
            
            ("Python equivalent of Java's ArrayList",
             "Python's list is equivalent to Java's ArrayList:\n\n```python\n# Create list\nmy_list = []  # or [1, 2, 3]\n\n# Add elements\nmy_list.append(10)  # like add()\n\n# Insert at index\nmy_list.insert(0, 5)  # like add(index, element)\n\n# Remove\nmy_list.remove(10)  # like remove(object)\ndel my_list[0]  # remove by index\n\n# Get size\nsize = len(my_list)  # like size()\n```",
             "java_arraylist"),
            
            ("Convert JavaScript Promise to Python equivalent",
             "Python's asyncio.Future is similar to JavaScript Promises:\n\n```python\nimport asyncio\n\nasync def fetch_data():\n    await asyncio.sleep(1)  # Simulated async operation\n    return 'Data loaded'\n\n# Usage\nresult = asyncio.run(fetch_data())\nprint(result)\n```\n\nFor simpler cases, use the requests library synchronously.",
             "js_promise"),
        ]
        
        generated_count = 0
        for instruction, response, subcategory in conversions:
            self.add_example(
                instruction=instruction,
                response=response,
                scope_label="answer_python_conversion",
                category="python_conversion",
                expected_behavior="answer"
            )
            generated_count += 1
            
            # Add variations
            variations = [
                instruction.replace("Convert", "Translate"),
                instruction.replace("How would I write", "Python equivalent of"),
                instruction.replace("this", "a"),
            ]
            
            variations_needed = min(count // len(conversions) - 1, 4)
            added = 0
            for var in variations:
                if var != instruction and added < variations_needed:
                    self.add_example(
                        instruction=var,
                        response=response,
                        scope_label="answer_python_conversion",
                        category="python_conversion",
                        expected_behavior="answer"
                    )
                    generated_count += 1
                    added += 1
        
        print(f"✓ Generated {len([e for e in self.examples if e['category'] == 'python_conversion'])} conversion examples")
    
    def generate_python_examples(self, count: int = 150):
        """Generate valid Python questions that MUST be answered"""
        
        python_questions = [
            ("How do I create a list in Python?",
             "You can create a list in Python using square brackets:\n\n```python\nmy_list = [1, 2, 3, 4, 5]\nempty_list = []\nmixed_list = [1, 'hello', 3.14, True]\n```\n\nLists are mutable and can contain items of different types.",
             "python_basics"),
            
            ("Write a Python function to reverse a string",
             "Here's a Python function to reverse a string:\n\n```python\ndef reverse_string(s):\n    return s[::-1]\n\n# Usage\nresult = reverse_string('hello')\nprint(result)  # Output: 'olleh'\n```\n\nThe [::-1] slice notation reverses the string efficiently.",
             "python_functions"),
            
            ("Explain Python decorators",
             "Python decorators are functions that modify the behavior of other functions. Here's a simple example:\n\n```python\ndef my_decorator(func):\n    def wrapper():\n        print('Before function call')\n        func()\n        print('After function call')\n    return wrapper\n\n@my_decorator\ndef say_hello():\n    print('Hello!')\n\nsay_hello()\n```\n\nDecorators are commonly used for logging, authentication, and timing functions.",
             "python_concepts"),
            
            ("What's the difference between list and tuple in Python?",
             "The main differences are:\n\n```python\n# List - mutable\nmy_list = [1, 2, 3]\nmy_list[0] = 10  # OK - can modify\nmy_list.append(4)  # OK - can add items\n\n# Tuple - immutable\nmy_tuple = (1, 2, 3)\n# my_tuple[0] = 10  # Error! Cannot modify\n# my_tuple.append(4)  # Error! No append method\n```\n\nUse lists when you need to modify data. Use tuples for fixed collections.",
             "python_basics"),
            
            ("How do I read a file in Python?",
             "You can read files in Python using the open() function:\n\n```python\n# Read entire file\nwith open('file.txt', 'r') as f:\n    content = f.read()\n    print(content)\n\n# Read line by line\nwith open('file.txt', 'r') as f:\n    for line in f:\n        print(line.strip())\n\n# Read all lines into a list\nwith open('file.txt', 'r') as f:\n    lines = f.readlines()\n```\n\nThe 'with' statement ensures the file is properly closed.",
             "python_file_io"),
            
            ("Create a Python class with constructor",
             "Here's how to create a Python class:\n\n```python\nclass Person:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n    \n    def greet(self):\n        return f'Hello, I am {self.name}'\n\n# Usage\nperson = Person('Alice', 30)\nprint(person.greet())\n```",
             "python_oop"),
            
            ("How do I handle exceptions in Python?",
             "Use try-except blocks:\n\n```python\ntry:\n    result = 10 / 0\nexcept ZeroDivisionError:\n    print('Cannot divide by zero')\nexcept Exception as e:\n    print(f'Error: {e}')\nfinally:\n    print('Cleanup code here')\n```",
             "python_exceptions"),
        ]
        
        generated_count = 0
        for instruction, response, subcategory in python_questions:
            self.add_example(
                instruction=instruction,
                response=response,
                scope_label="answer_python",
                category="python_programming",
                expected_behavior="answer"
            )
            generated_count += 1
            
            # Add variations
            variations = [
                instruction.replace("How do I", "How can I"),
                instruction.replace("Write", "Create"),
                instruction.replace("Explain", "What are"),
            ]
            
            variations_needed = min(count // len(python_questions) - 1, 4)
            added = 0
            for var in variations:
                if var != instruction and added < variations_needed:
                    self.add_example(
                        instruction=var,
                        response=response,
                        scope_label="answer_python",
                        category="python_programming",
                        expected_behavior="answer"
                    )
                    generated_count += 1
                    added += 1
        
        print(f"✓ Generated {len([e for e in self.examples if e['category'] == 'python_programming'])} Python examples")
    
    def generate_refusal_examples(self, count: int = 150):
        """Generate non-programming refusal examples"""
        
        non_programming = [
            ("What is the capital of France?", "geography"),
            ("How do I cook pasta?", "cooking"),
            ("Who won the 2020 Olympics?", "sports"),
            ("Tell me about Greek mythology", "mythology"),
            ("What are the health benefits of yoga?", "health"),
            ("Write a poem about the ocean", "creative writing"),
            ("How do I lose weight?", "health advice"),
            ("What's the weather like in London?", "weather"),
            ("Recommend a good restaurant in Tokyo", "recommendations"),
            ("What's the meaning of life?", "philosophy"),
        ]
        
        for instruction, topic in non_programming:
            template = random.choice(self.refusal_templates)
            response = template.format(topic_area=topic)
            
            self.add_example(
                instruction=instruction,
                response=response,
                scope_label="refuse_non_programming",
                category="non_programming",
                expected_behavior="refuse"
            )
        
        print(f"✓ Generated {len([e for e in self.examples if e['category'] == 'non_programming'])} refusal examples")
    
    def save_dataset(self, output_dir: Path):
        """Save generated dataset"""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save full dataset
        output_file = output_dir / "training_candidate.jsonl"
        with open(output_file, 'w', encoding='utf-8') as f:
            for example in self.examples:
                f.write(json.dumps(example, ensure_ascii=False) + '\n')
        
        print(f"\n✓ Saved {len(self.examples)} examples to {output_file}")
        
        # Generate statistics
        self.print_statistics()
    
    def print_statistics(self):
        """Print dataset statistics"""
        print("\n" + "="*70)
        print("DATASET STATISTICS")
        print("="*70)
        
        # Total count
        print(f"\nTotal Examples: {len(self.examples)}")
        
        # By category
        categories = Counter([e['category'] for e in self.examples])
        print("\nBy Category:")
        for cat, count in categories.most_common():
            pct = count / len(self.examples) * 100
            print(f"  {cat:40s}: {count:4d} ({pct:5.1f}%)")
        
        # By expected behavior
        behaviors = Counter([e['expected_behavior'] for e in self.examples])
        print("\nBy Expected Behavior:")
        for beh, count in behaviors.most_common():
            pct = count / len(self.examples) * 100
            print(f"  {beh:10s}: {count:4d} ({pct:5.1f}%)")
        
        # Response diversity
        responses = [e['response'] for e in self.examples]
        unique_responses = len(set(responses))
        print(f"\nResponse Diversity:")
        print(f"  Unique responses: {unique_responses} ({unique_responses/len(self.examples)*100:.1f}%)")
        
        # Instruction diversity
        instructions = [e['instruction'] for e in self.examples]
        unique_instructions = len(set(instructions))
        duplicates = len(instructions) - unique_instructions
        print(f"\nInstruction Diversity:")
        print(f"  Unique instructions: {unique_instructions} ({unique_instructions/len(self.examples)*100:.1f}%)")
        print(f"  Duplicate instructions: {duplicates}")


def main():
    print("="*70)
    print("PHASE 6F: HIGH-QUALITY DATASET GENERATION")
    print("="*70)
    
    generator = DatasetGenerator()
    
    # Generate dataset following distribution
    print("\nGenerating dataset...")
    print("-" * 70)
    
    # Target: ~1500 examples total
    # 35% redirect examples (~525)
    generator.generate_redirect_examples(count=525)
    
    # 20% interoperability examples (~300)
    generator.generate_interoperability_examples(count=300)
    
    # 15% comparison examples (~225)
    generator.generate_comparison_examples(count=225)
    
    # 10% conversion examples (~150)
    generator.generate_conversion_examples(count=150)
    
    # 10% Python examples (~150)
    generator.generate_python_examples(count=150)
    
    # 10% refusal examples (~150)
    generator.generate_refusal_examples(count=150)
    
    # Save dataset
    output_dir = Path("datasets/phase6e/generated")
    generator.save_dataset(output_dir)
    
    print("\n" + "="*70)
    print("DATASET GENERATION COMPLETE")
    print("="*70)
    print(f"\nTotal examples generated: {len(generator.examples)}")
    print("Next: Run validation script (validate_phase6e_dataset.py)")


if __name__ == "__main__":
    main()
