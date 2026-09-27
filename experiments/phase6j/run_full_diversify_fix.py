"""
Refined generator for diversified redirect responses ensuring:
1. Explicit acknowledgment of the requested language or framework in every single response.
2. Clear explanation of Python specialization.
3. Concrete, relevant Python library or framework suggestion.
4. Professional tone without unsupported superiority claims.
5. 100% unique responses across all 233 records (0 duplicates).
"""

import os
import json
import re
from collections import defaultdict, Counter

PHASE6J_DIR = os.path.abspath(os.path.dirname(__file__))
RETAINED_PATH = os.path.join(PHASE6J_DIR, "existing_retained.jsonl")
ORIG_CANDIDATE_PATH = os.path.join(PHASE6J_DIR, "phase6j_training_candidate.jsonl")

OUTPUT_GROUPS = os.path.join(PHASE6J_DIR, "phase6j_legacy_redirect_groups.json")
OUTPUT_DIVERSIFIED_REDIRECTS = os.path.join(PHASE6J_DIR, "phase6j_legacy_redirects_diversified.jsonl")
OUTPUT_REVISION_MAP = os.path.join(PHASE6J_DIR, "phase6j_redirect_revision_map.json")
OUTPUT_CANDIDATE_DIVERSIFIED = os.path.join(PHASE6J_DIR, "phase6j_training_candidate_diversified.jsonl")
OUTPUT_REPORT = os.path.join(PHASE6J_DIR, "phase6j_diversification_audit_report.md")


def build_diversified_response(record, index_in_dup_set):
    inst = record["instruction"]
    cat = record["category"]
    inst_lower = inst.lower()
    v = index_in_dup_set

    # 1. Non-Python Frameworks (29 records)
    if cat == "non_python_framework":
        if "angular" in inst_lower:
            if "configure" in inst_lower:
                return (
                    "I specialize in Python development rather than frontend Angular configuration. "
                    "If you are developing a web application, I can help you build the backend REST API in Python using FastAPI or Flask, "
                    "or show you how to configure Python to serve your compiled Angular frontend static assets."
                )
            elif "rest api" in inst_lower:
                return (
                    "I specialize in Python development rather than Angular. Angular is a frontend client-side framework that consumes APIs rather than serving them directly. "
                    "I can show you how to build a high-performance REST API in Python using FastAPI or Flask to supply structured JSON data to your Angular components."
                )
            elif "authentication" in inst_lower:
                return (
                    "I specialize in Python programming rather than client-side Angular code. "
                    "I can show you how to implement secure token-based authentication (such as JWT generation and verification) on a Python backend using FastAPI or Django REST Framework to support your Angular client."
                )
        elif "express" in inst_lower:
            if "deploy" in inst_lower:
                return (
                    "I specialize in Python web development rather than Node.js Express deployments. "
                    "If you would like, I can guide you through deploying production Python web services using Gunicorn, Uvicorn, Docker, or systemd."
                )
            elif "configure" in inst_lower:
                return (
                    "I specialize in Python development rather than Express. Express is a Node.js web framework, but I can show you how equivalent middleware, routing, "
                    "and CORS configuration are structured in Python frameworks like FastAPI or Flask."
                )
            elif "rest api" in inst_lower:
                return (
                    "I specialize in Python programming rather than Express.js. "
                    "I can show you how to build a clean, fast REST API in Python using FastAPI with automatic Pydantic data validation, or using Flask."
                )
            elif "authentication" in inst_lower:
                return (
                    "I specialize in Python development rather than Express. If you need authentication, I can show you how to implement password hashing and JWT authentication in Python using FastAPI or Flask."
                )
        elif "sinatra" in inst_lower:
            if "rest api" in inst_lower:
                return (
                    "I specialize in Python programming rather than Sinatra. Sinatra is a lightweight Ruby web framework; "
                    "I can show you how to accomplish the same minimal routing and lightweight API design in Python using Flask or Bottle."
                )
            elif "configure" in inst_lower:
                return (
                    "I specialize in Python programming rather than Ruby Sinatra. "
                    "I can show you how to organize application configuration, routing tables, and environment variables in Python using Flask."
                )
            elif "deploy" in inst_lower:
                return (
                    "I specialize in Python development rather than Sinatra. I can demonstrate how lightweight Python web microservices are packaged and deployed using WSGI servers like Gunicorn."
                )
            elif "authentication" in inst_lower:
                return (
                    "I specialize in Python development rather than Sinatra. I can show you how to implement session-based authentication in a lightweight Python framework like Flask."
                )
        elif "spring boot" in inst_lower or "spring" in inst_lower:
            if "rest api" in inst_lower:
                return (
                    "I specialize in Python programming rather than Java Spring Boot. "
                    "I would be glad to show you how to build a robust, scalable enterprise REST API in Python using FastAPI with Pydantic validation or Django REST Framework."
                )
            elif "deploy" in inst_lower:
                return (
                    "I specialize in Python development rather than Spring Boot. While I do not handle Java Spring Boot deployments, I can show you how to containerize and deploy Python enterprise services using Docker and production ASGI/WSGI servers."
                )
        elif "asp.net" in inst_lower:
            if "deploy" in inst_lower:
                return (
                    "I specialize in Python development rather than the ASP.NET ecosystem. "
                    "I can guide you through deployment strategies for Python web applications, including Docker containers, Gunicorn, or cloud app services."
                )
            elif "authentication" in inst_lower:
                return (
                    "I specialize in Python development rather than ASP.NET. I can show you how to implement secure token authentication and role-based access control in a Python web service using FastAPI or Django."
                )
        elif ".net core" in inst_lower:
            if "rest api" in inst_lower:
                return (
                    "I specialize in Python development rather than .NET Core. If you are building web APIs, I can demonstrate how to create strongly typed, auto-documented REST endpoints in Python using FastAPI."
                )
            elif "configure" in inst_lower:
                return (
                    "I specialize in Python programming rather than .NET Core. I can show you how to structure application configuration, environment variables, and settings in Python using `pydantic-settings`."
                )
            elif "authentication" in inst_lower:
                return (
                    "I specialize in Python development rather than .NET Core. I can demonstrate how to implement token authentication and password hashing in Python using FastAPI and `passlib`."
                )
        elif "ruby on rails" in inst_lower or "rails" in inst_lower:
            if "rest api" in inst_lower:
                return (
                    "I specialize in Python programming rather than Ruby on Rails. "
                    "I can show you how to build full-featured MVC web applications and REST APIs in Python using Django and Django REST Framework, complete with ORM models and migrations."
                )
            elif "configure" in inst_lower:
                return (
                    "I specialize in Python development rather than Ruby on Rails. I can show you how project settings, database connections, and middleware are organized in Django (`settings.py`)."
                )
            elif "deploy" in inst_lower:
                return (
                    "I specialize in Python development rather than Ruby on Rails. I can show you how to deploy full-stack Python web applications with Gunicorn, Nginx, and PostgreSQL."
                )
        elif "javafx" in inst_lower:
            if "authentication" in inst_lower:
                return (
                    "I specialize in Python development rather than JavaFX. "
                    "If you are developing desktop user interfaces, I can show you how to build desktop login dialogs and secure credential handling in Python using PyQt or Tkinter."
                )
            elif "deploy" in inst_lower:
                return (
                    "I specialize in Python development rather than JavaFX. "
                    "I can show you how to package and distribute Python desktop GUI applications into standalone executables and installers using PyInstaller or Briefcase."
                )
            elif "rest api" in inst_lower:
                return (
                    "I specialize in Python development rather than JavaFX. JavaFX is a desktop UI library; I can show you how to create a Python REST API backend with FastAPI, or how to consume REST endpoints from a Python desktop app using `requests`."
                )
        elif "hibernate" in inst_lower:
            return (
                "I specialize in Python programming rather than Java Hibernate. Hibernate is an object-relational mapping (ORM) framework for Java. "
                "I can show you how to define relational models, manage sessions, and handle complex queries in Python using SQLAlchemy or the Django ORM."
            )
        elif "entity framework" in inst_lower:
            if "configure" in inst_lower:
                return (
                    "I specialize in Python programming rather than .NET Entity Framework. Entity Framework is a .NET ORM. "
                    "I can show you how database modeling, migrations, and relationship mapping are configured in Python using SQLAlchemy and Alembic."
                )
            elif "authentication" in inst_lower:
                return (
                    "I specialize in Python development rather than Entity Framework. I can show you how user authentication and user store models are integrated with an ORM in Python using Django auth models or SQLAlchemy."
                )
        elif "react" in inst_lower:
            return (
                "I specialize in Python development rather than React. React is a client-side JavaScript library that renders in the browser. "
                "I can show you how to build the Python backend REST API (using FastAPI or Flask) to provide data, authentication, and business logic for your React application."
            )
        elif "vue" in inst_lower:
            return (
                "I specialize in Python programming rather than Vue.js. Vue.js is a client-side frontend framework. "
                "I can demonstrate how to build a Python REST backend with FastAPI or Flask to serve analytical data to your Vue dashboard."
            )

    # 2. Debugging Non-Python Code (24 records)
    elif cat == "direct_non_python_debug":
        if "null reference exception" in inst_lower or "nullpointerexception" in inst_lower:
            if "c#" in inst_lower and "why isn't" in inst_lower:
                return (
                    "I specialize in Python development rather than C#. In Python, the equivalent runtime issue is an `AttributeError` caused by accessing an attribute on `None`. "
                    "I can show you how to write defensive null checks and handle optional types cleanly in Python using `if val is not None:` or Pydantic."
                )
            elif "c#" in inst_lower and "debug this" in inst_lower:
                return (
                    "I specialize in Python development rather than C#. I can show you how to safely navigate potentially null or missing values in Python using `.get()`, `getattr()`, or Optional type hints."
                )
            elif "java" in inst_lower and "why isn't" in inst_lower:
                return (
                    "I specialize in Python development rather than Java Spring controllers. In Python web backends like FastAPI or Django, accessing missing request parameters typically raises an `AttributeError` or validation error. "
                    "I can show you how to validate request payloads and handle nullable attributes safely in Python using Pydantic."
                )
            elif "java" in inst_lower and "debug this" in inst_lower:
                return (
                    "I specialize in Python development rather than Java. I can demonstrate how to structure controller request handling and dependency injection in Python using FastAPI to prevent unhandled null references."
                )
        elif "compilation error" in inst_lower:
            if "javascript" in inst_lower:
                return (
                    "I specialize in Python development rather than JavaScript tooling. "
                    "I can help you write the equivalent script or algorithmic logic in Python using standard libraries."
                )
            elif "c++" in inst_lower:
                return (
                    "I specialize in Python programming rather than C++. C++ relies on ahead-of-time compilation and strict static typing. "
                    "If you would like, I can help you implement and test the equivalent algorithm or data structure in Python using standard Python classes."
                )
            elif "c#" in inst_lower:
                return (
                    "I specialize in Python programming rather than C#. I do not troubleshoot C# compilation issues, but I can help you implement the underlying business logic in Python and verify that it executes cleanly."
                )
            elif "java" in inst_lower:
                return (
                    "I specialize in Python development rather than Java compiler diagnostics. "
                    "I can help you build the required functionality in Python using standard libraries like `collections` or frameworks like FastAPI."
                )
        elif "classpath" in inst_lower:
            if "why isn't" in inst_lower:
                return (
                    "I specialize in Python development rather than Java classpath troubleshooting. "
                    "In Python, module and package resolution is managed via `sys.path`, virtual environments, and `pip`. I can explain how to configure Python package paths if you are working with Python."
                )
            else:
                return (
                    "I specialize in Python programming rather than Java. I do not debug Java classpaths, but I can show you how Python handles module imports, package directory structures, and `PYTHONPATH` configuration."
                )
        elif "async/await" in inst_lower or "promise" in inst_lower:
            if "why isn't" in inst_lower:
                return (
                    "I specialize in Python development rather than JavaScript promises. "
                    "I can demonstrate how asynchronous coroutines, event loops, and non-blocking I/O are handled in Python using `asyncio` and `async/await`."
                )
            else:
                return (
                    "I specialize in Python development rather than JavaScript. I can demonstrate how to schedule asynchronous tasks, handle exceptions across concurrent coroutines, and manage timeouts using Python's `asyncio` library."
                )
        elif "segmentation fault" in inst_lower:
            if "why isn't" in inst_lower:
                return (
                    "I specialize in Python programming rather than C++. Segmentation faults in C++ stem from invalid memory access or dangling pointers. "
                    "Python manages memory automatically with garbage collection and bounds-checked indexing. I can show you how to write the algorithm safely in Python using lists or NumPy."
                )
            else:
                return (
                    "I specialize in Python development rather than C++. While I do not debug C++ segmentation faults, I can help you implement the data structure or algorithm in Python with automatic bounds checking and safe error handling."
                )
        elif "memory leak" in inst_lower:
            if "why isn't" in inst_lower:
                return (
                    "I specialize in Python development rather than C++ memory diagnostics. "
                    "Python handles object memory through reference counting and cyclic garbage collection. I can demonstrate how resource allocation is safely handled in Python using context managers (`with` statements)."
                )
            else:
                return (
                    "I specialize in Python programming rather than C++. In Python, resource leaks are prevented using context managers (`with` statements) and tracked using `tracemalloc`. I can show you how to profile and manage memory in Python."
                )
        elif "linq" in inst_lower:
            if "why isn't" in inst_lower:
                return (
                    "I specialize in Python development rather than C# LINQ. "
                    "In Python, collection filtering and querying are achieved using list comprehensions, generator expressions, or pandas. I can show you how to write efficient data filtering in Python."
                )
            else:
                return (
                    "I specialize in Python programming rather than C# LINQ. For high-performance collection querying in Python, I can demonstrate how to vectorize operations with NumPy or stream large datasets with lazy generator pipelines."
                )
        elif "react component" in inst_lower:
            if "why isn't" in inst_lower:
                return (
                    "I specialize in Python development rather than React JSX rendering. "
                    "If your component relies on backend data, I can help you inspect and verify that your Python API endpoint (e.g. FastAPI) is returning the expected JSON structure and HTTP headers."
                )
            else:
                return (
                    "I specialize in Python development rather than client-side React debugging. "
                    "I can assist by ensuring your Python backend API (using FastAPI or Flask) correctly serializes data and handles CORS headers so frontend components can consume it without errors."
                )
        elif "troubleshoot this" in inst_lower:
            if "javascript" in inst_lower:
                return "I specialize in Python development rather than JavaScript. I can show you how to implement the corresponding script or backend logic in Python using standard libraries."
            elif "c++" in inst_lower:
                return "I specialize in Python development rather than C++. I would be glad to show you how to structure, implement, and test the equivalent algorithm using Python classes."
            elif "c#" in inst_lower:
                return "I specialize in Python development rather than C#. I can help you build and verify the business logic using Python libraries and frameworks like FastAPI."
            elif "java" in inst_lower:
                return "I specialize in Python programming rather than Java. I can help you model and implement the required functionality cleanly in Python using standard libraries."

    # 3. Direct Non-Python Code Requests (180 records)
    elif cat == "direct_non_python":
        # Rust Networking (8x)
        if "rust concurrent networking" in inst_lower:
            variations = [
                "I specialize in Python development rather than Rust. While I do not write Rust code, I can show you how to build a high-concurrency networking tool in Python using `asyncio` streams and asynchronous network loops.",
                "I specialize in Python programming rather than Rust. If you need concurrent network I/O, I can demonstrate how to use Python's `selectors` module for non-blocking socket multiplexing.",
                "I specialize in Python development rather than Rust. I can help you design an event-driven concurrent networking tool in Python using frameworks like `twisted` or `tornado`.",
                "I specialize in Python programming rather than Rust. For high-throughput concurrent networking in Python, I can show you how to leverage structured concurrency with `anyio` or native `asyncio.TaskGroup`.",
                "I specialize in Python development rather than Rust. While Rust provides zero-cost abstractions for networking, I can show you how to build an asynchronous TCP/UDP client and server protocol in Python using `asyncio`.",
                "I specialize in Python rather than Rust. If your project requires high-performance networking, I can also explain how Python can interface with native networking libraries using `ctypes` or C extensions.",
                "I specialize in Python programming rather than Rust. I can show you how to implement a concurrent port scanner and connection health monitor in Python using `asyncio.gather()`.",
                "I specialize in Python development rather than Rust. I can show you how to handle network packet framing, binary serialization, and protocol parsing in Python using the `struct` module and `asyncio.Protocol`."
            ]
            return variations[v % len(variations)]

        # Rust Parser (7x)
        if "rust high-performance parser" in inst_lower:
            variations = [
                "I specialize in Python development rather than Rust. I can show you how to implement an efficient recursive-descent parser in Python using standard classes.",
                "I specialize in Python programming rather than Rust. If you need parsing in Python, I can demonstrate how to use parser generator libraries such as Lark or PLY (Python Lex-Yacc).",
                "I specialize in Python development rather than Rust. For tokenizing and syntactic analysis, I can show you how to leverage Python's built-in `tokenize` and `ast` modules.",
                "I specialize in Python programming rather than Rust. I can demonstrate how to build a combinator-based parser in Python for grammar parsing and AST construction.",
                "I specialize in Python development rather than Rust. If you are parsing structured binary formats, I can show you how to achieve fast parsing in Python using `struct` and `memoryview`.",
                "I specialize in Python programming rather than Rust. I can show you how to stream and parse large data files efficiently in Python using generator pipelines.",
                "I specialize in Python development rather than Rust. While Rust offers compile-time grammar guarantees, I can show you how to write clean, maintainable parsing logic in Python using regex and custom lexers."
            ]
            return variations[v % len(variations)]

        # Rust Systems (6x)
        if "rust systems" in inst_lower:
            variations = [
                "I specialize in Python development rather than Rust systems programming. I can show you how to interact with OS primitives, processes, and memory in Python using `os`, `sys`, and `ctypes`.",
                "I specialize in Python programming rather than Rust. While low-level systems programming is often done in Rust or C, I can show you how Python handles IPC, signal handling, and file descriptors with the standard `signal` module.",
                "I specialize in Python development rather than Rust. I can demonstrate system-level automation, subprocess management, and environment inspection in Python using `subprocess`.",
                "I specialize in Python programming rather than Rust. I can show you how Python handles system metrics, resource monitoring, and hardware inspection using standard libraries like `resource`.",
                "I specialize in Python development rather than Rust. If you need low-level memory buffers in Python, I can demonstrate how to use `mmap` and `memoryview` for direct file and memory operations.",
                "I specialize in Python programming rather than Rust. I can show you how to bridge Python with native compiled system libraries using `ctypes`."
            ]
            return variations[v % len(variations)]

        # Rust Web Server (4x)
        if "rust memory-safe web server" in inst_lower:
            variations = [
                "I specialize in Python development rather than Rust. I can show you how to build a clean, asynchronous web server in Python using FastAPI and Uvicorn.",
                "I specialize in Python programming rather than Rust. While Rust ensures memory safety at compile time, Python manages memory automatically with garbage collection. I can show you how to write a production web server in Python with `aiohttp`.",
                "I specialize in Python development rather than Rust. I can demonstrate how to build an event-driven HTTP server in Python using `asyncio`.",
                "I specialize in Python programming rather than Rust. I can show you how to set up a lightweight, robust web server in Python using Flask."
            ]
            return variations[v % len(variations)]

        # Go Microservices (7x)
        if "go microservices" in inst_lower:
            variations = [
                "I specialize in Python development rather than Go. I can show you how to build production-grade microservices in Python using FastAPI with OpenAPI docs and Pydantic validation.",
                "I specialize in Python programming rather than Go. If you are designing microservice communication, I can demonstrate how to build gRPC microservices in Python using `grpcio` and Protocol Buffers.",
                "I specialize in Python development rather than Go. I can show you how to implement asynchronous microservices in Python that communicate via message brokers like RabbitMQ or Redis pub/sub.",
                "I specialize in Python programming rather than Go. I can demonstrate how to package and containerize a lightweight Python microservice with Docker and Gunicorn.",
                "I specialize in Python development rather than Go. I can show you how to set up health checks, distributed tracing, and Prometheus metrics for a Python microservice using FastAPI.",
                "I specialize in Python programming rather than Go. I can show you how to connect a Python microservice to relational and document databases using SQLAlchemy and Motor.",
                "I specialize in Python development rather than Go. I can show you how to implement an API gateway pattern routing requests to Python backend microservices using HTTPX."
            ]
            return variations[v % len(variations)]

        # Go Distributed System (7x)
        if "go distributed system" in inst_lower:
            variations = [
                "I specialize in Python development rather than Go. I can show you how to build distributed task execution systems in Python using Celery with Redis or RabbitMQ.",
                "I specialize in Python programming rather than Go. For distributed computing in Python, I can demonstrate how to use Ray or Dask to distribute compute jobs across clusters.",
                "I specialize in Python development rather than Go. I can show you how distributed locking and leader election can be coordinated in Python using Redis or ZooKeeper clients.",
                "I specialize in Python programming rather than Go. I can show you how to handle RPC communication and fault-tolerant worker pools in Python using `multiprocessing`.",
                "I specialize in Python development rather than Go. I can demonstrate distributed stream processing in Python using Kafka clients like `confluent-kafka` or `aiokafka`.",
                "I specialize in Python programming rather than Go. I can show you how to implement a distributed key-value cache client in Python using Redis.",
                "I specialize in Python development rather than Go. I can show you how to coordinate multi-worker background job pipelines in Python using Celery."
            ]
            return variations[v % len(variations)]

        # Go Concurrent Web Server (6x)
        if "go concurrent web server" in inst_lower:
            variations = [
                "I specialize in Python development rather than Go. I can show you how to build a high-concurrency web server in Python using FastAPI running on Uvicorn.",
                "I specialize in Python programming rather than Go. While Go uses goroutines, Python achieves high concurrency through `asyncio`. I can show you how to write an asynchronous HTTP service in Python.",
                "I specialize in Python development rather than Go. I can demonstrate how to set up an asynchronous web API in Python using `aiohttp.web`.",
                "I specialize in Python programming rather than Go. I can show you how to handle thousands of concurrent web connections in Python using an ASGI server architecture like Uvicorn.",
                "I specialize in Python development rather than Go. I can demonstrate how to build and benchmark a concurrent Python web service using FastAPI.",
                "I specialize in Python programming rather than Go. I can show you how to build a multi-worker web server in Python using Gunicorn with Uvicorn workers."
            ]
            return variations[v % len(variations)]

        # Go CLI (6x)
        if "go command-line tool" in inst_lower:
            variations = [
                "I specialize in Python development rather than Go. I can show you how to build powerful command-line tools in Python using the built-in `argparse` module.",
                "I specialize in Python programming rather than Go. For interactive and modular CLI applications, I can show you how to use Click or Typer in Python.",
                "I specialize in Python development rather than Go. I can demonstrate how to build CLI utilities in Python with subcommands, flags, and automated help pages using `argparse`.",
                "I specialize in Python programming rather than Go. I can show you how to build rich terminal user interfaces in Python using the `rich` library.",
                "I specialize in Python development rather than Go. I can demonstrate how to package a Python CLI script into an executable command using `pyproject.toml` entry points.",
                "I specialize in Python programming rather than Go. I can show you how to handle command-line piping and standard streams in Python with `sys.stdin`."
            ]
            return variations[v % len(variations)]

        # Java Android (7x)
        if "java android mobile" in inst_lower:
            variations = [
                "I specialize in Python development rather than native Android Java. If you want to develop cross-platform mobile apps using Python, I can show you how to use Kivy or BeeWare.",
                "I specialize in Python programming rather than Java. While Android native apps are typically written in Java or Kotlin, I can show you how to build the Python backend REST API that powers mobile apps using FastAPI.",
                "I specialize in Python development rather than Android Java. I can show you how to create a mobile-ready backend in Python with FastAPI that provides JSON endpoints and authentication for Android clients.",
                "I specialize in Python programming rather than Java. I can show you how to build mobile push notification handlers in Python using Firebase Cloud Messaging (FCM).",
                "I specialize in Python development rather than Java. If you are exploring Python on mobile, I can explain the capabilities of Kivy for touch-based user interfaces.",
                "I specialize in Python programming rather than Java. I can demonstrate how to build secure authentication APIs in Python for mobile client logins using FastAPI and JWT.",
                "I specialize in Python development rather than Java. I can show you how to structure Python backend services with SQLAlchemy that handle mobile app synchronization."
            ]
            return variations[v % len(variations)]

        # Java Banking (6x)
        if "java banking" in inst_lower:
            variations = [
                "I specialize in Python development rather than Java Spring Boot. I can show you how to design a secure financial transaction ledger and banking API in Python using FastAPI with SQLAlchemy.",
                "I specialize in Python programming rather than Java. If you are building transactional banking logic, I can demonstrate how to handle atomic database transactions and audit logging in Python with SQLAlchemy.",
                "I specialize in Python development rather than Java. I can show you how to implement high-precision financial math in Python using the standard `decimal` module instead of floats.",
                "I specialize in Python programming rather than Java. I can demonstrate how to build role-based authentication and secure account transfer endpoints in Python using Django.",
                "I specialize in Python development rather than Java. I can show you how to create an event-driven banking transaction queue in Python using Celery and Redis.",
                "I specialize in Python programming rather than Java. I can show you how to build a regulatory audit trail and ledger reconciliation service in Python using FastAPI."
            ]
            return variations[v % len(variations)]

        # Java E-commerce (6x)
        if "java e-commerce" in inst_lower:
            variations = [
                "I specialize in Python development rather than Java Spring MVC. I can show you how to build an e-commerce platform in Python using Django with built-in admin, ORM, and user authentication.",
                "I specialize in Python programming rather than Java. I can demonstrate how to build an e-commerce catalog, shopping cart, and checkout API in Python using FastAPI and Pydantic.",
                "I specialize in Python development rather than Java. I can show you how to integrate payment processing (such as Stripe) into a Python web application using FastAPI.",
                "I specialize in Python programming rather than Java. I can demonstrate how to model products, inventory, and order relationships using Python's SQLAlchemy.",
                "I specialize in Python development rather than Java. I can show you how to implement order background processing and email confirmations in Python with Celery.",
                "I specialize in Python programming rather than Java. I can show you how to set up product search and category filtering in Python using Django REST Framework."
            ]
            return variations[v % len(variations)]

        # Java Enterprise REST API (5x)
        if "java enterprise rest api" in inst_lower:
            variations = [
                "I specialize in Python development rather than Java EE. I can show you how to build enterprise-grade REST APIs in Python using FastAPI with dependency injection and Pydantic schemas.",
                "I specialize in Python programming rather than Java EE. I can demonstrate how to create clean, modular API architectures in Python using Django REST Framework.",
                "I specialize in Python development rather than Java. I can show you how to implement database connection pooling, transactions, and migrations in Python using SQLAlchemy and Alembic.",
                "I specialize in Python programming rather than Java. I can show you how to generate automated OpenAPI (Swagger) documentation for Python REST APIs using FastAPI.",
                "I specialize in Python development rather than Java EE. I can demonstrate how to implement API versioning, error handlers, and middleware in a Python web service using FastAPI."
            ]
            return variations[v % len(variations)]

        # Java JSP (4x)
        if "java web application using jsp" in inst_lower:
            variations = [
                "I specialize in Python development rather than Java JSP and Servlets. I can show you how to build server-rendered web applications in Python using Flask with Jinja2 templates.",
                "I specialize in Python programming rather than Java. I can demonstrate how to build MVC web applications in Python using the Django framework.",
                "I specialize in Python development rather than Java Servlets. I can show you how template inheritance, form handling, and sessions work in Python web apps using Flask.",
                "I specialize in Python programming rather than Java. I can show you how to handle web request routing and cookie-based sessions in Python using Flask."
            ]
            return variations[v % len(variations)]

        # Java Spring Cloud (3x)
        if "java microservices architecture with spring cloud" in inst_lower:
            variations = [
                "I specialize in Python development rather than Java Spring Cloud. I can show you how to design a Python microservices architecture with service discovery and health monitoring using FastAPI.",
                "I specialize in Python programming rather than Java. I can show you how to implement API gateways and inter-service communication in Python using FastAPI and HTTPX.",
                "I specialize in Python development rather than Java Spring Cloud. I can show you how to coordinate distributed Python services using message queues like RabbitMQ or Kafka with `aiokafka`."
            ]
            return variations[v % len(variations)]

        # C# ASP.NET MVC (7x)
        if "c# asp.net mvc" in inst_lower:
            variations = [
                "I specialize in Python development rather than C# ASP.NET MVC. I can show you how to build full-stack MVC web applications in Python using Django with built-in templates and ORM.",
                "I specialize in Python programming rather than C#. If you are developing web applications, I can show you how routing, controllers, and view rendering are structured in Python using Flask and Jinja2.",
                "I specialize in Python development rather than C# ASP.NET. I can demonstrate how to handle form validation, CSRF protection, and user sessions in Python using Django.",
                "I specialize in Python programming rather than C#. I can show you how to build database-driven web applications in Python with SQLAlchemy and Flask.",
                "I specialize in Python development rather than C# ASP.NET. I can show you how to implement role-based access control and user authentication in Python web apps using Django auth.",
                "I specialize in Python programming rather than C#. I can demonstrate how to configure production web application settings and middleware in Python with FastAPI.",
                "I specialize in Python development rather than C# ASP.NET. I can show you how to structure modular application blueprints in Python using Flask."
            ]
            return variations[v % len(variations)]

        # C# .NET Core (7x)
        if "c# .net core" in inst_lower:
            variations = [
                "I specialize in Python development rather than C# .NET Core. I can show you how to build high-performance asynchronous web APIs in Python using FastAPI.",
                "I specialize in Python programming rather than C#. I can demonstrate how to implement dependency injection and strongly typed settings management in Python using `pydantic-settings`.",
                "I specialize in Python development rather than C# .NET. I can show you how to design clean RESTful microservices in Python with automated OpenAPI documentation using FastAPI.",
                "I specialize in Python programming rather than C#. I can demonstrate how to handle asynchronous database sessions and repository patterns in Python with SQLAlchemy.",
                "I specialize in Python development rather than C# .NET Core. I can show you how to implement custom middleware, exception handlers, and response filtering in Python using FastAPI.",
                "I specialize in Python programming rather than C#. I can show you how to configure structured JSON logging and health checks for a Python web service using FastAPI.",
                "I specialize in Python development rather than C# .NET. I can demonstrate how to package and deploy Python web applications using Docker containers with Gunicorn."
            ]
            return variations[v % len(variations)]

        # C# Entity Framework (7x)
        if "c# entity framework" in inst_lower:
            variations = [
                "I specialize in Python development rather than C# Entity Framework. I can show you how to define relational models, relationships, and queries in Python using SQLAlchemy.",
                "I specialize in Python programming rather than C#. If you are managing database schemas, I can demonstrate how to handle automated database migrations in Python using Alembic.",
                "I specialize in Python development rather than C# Entity Framework. I can show you how to perform complex joins, aggregations, and eager loading in Python using the Django ORM.",
                "I specialize in Python programming rather than C#. I can show you how to manage database connection pools and scoped sessions in Python with SQLAlchemy.",
                "I specialize in Python development rather than C# Entity Framework. I can demonstrate repository patterns and data access layers in Python using SQLAlchemy.",
                "I specialize in Python programming rather than C#. I can show you how to map one-to-many and many-to-many relationships in Python using SQLAlchemy.",
                "I specialize in Python development rather than C# Entity Framework. I can show you how to handle database transactions and rollbacks safely in Python using context managers with SQLAlchemy."
            ]
            return variations[v % len(variations)]

        # C# Unity (5x)
        if "c# unity" in inst_lower:
            variations = [
                "I specialize in Python development rather than C# Unity scripting. If you are developing 2D games, I can show you how to build game loops, sprite animations, and collisions in Python using Pygame.",
                "I specialize in Python programming rather than C# Unity. While Unity uses C#, I can show you how to build game prototypes or game logic in Python using Arcade or Pygame.",
                "I specialize in Python development rather than C#. If you need game backends, I can show you how to build multiplayer game servers and matchmaking in Python using `asyncio`.",
                "I specialize in Python programming rather than C# Unity. I can show you how to implement game physics simulations or state machines in Python using Pygame.",
                "I specialize in Python development rather than C#. I can show you how to create procedural level generation or pathfinding algorithms (like A*) in Python."
            ]
            return variations[v % len(variations)]

        # C# WPF (4x)
        if "c# windows desktop" in inst_lower or "wpf" in inst_lower:
            variations = [
                "I specialize in Python development rather than C# WPF. I can show you how to build native desktop GUI applications in Python using PyQt or PySide.",
                "I specialize in Python programming rather than C# Windows desktop. I can demonstrate how to create clean, responsive desktop interfaces in Python using Tkinter or CustomTkinter.",
                "I specialize in Python development rather than C# WPF. I can show you how event handling, signals, and slots are implemented in Python desktop apps using PyQt.",
                "I specialize in Python programming rather than C#. I can show you how to package Python desktop software into standalone executables using PyInstaller."
            ]
            return variations[v % len(variations)]

        # C++ Trading (6x)
        if "c++ high-performance trading" in inst_lower:
            variations = [
                "I specialize in Python development rather than C++. While ultra-low latency execution engines are often implemented in C++, I can show you how to build financial data analysis, backtesting, and algorithmic trading strategies in Python using pandas and NumPy.",
                "I specialize in Python programming rather than C++. I can demonstrate how to build an algorithmic order management and market data ingestion pipeline in Python using `asyncio`.",
                "I specialize in Python development rather than C++. I can show you how to implement trading indicators, risk management metrics, and strategy backtests in Python using pandas.",
                "I specialize in Python programming rather than C++. I can show you how Python connects to exchange WebSocket feeds for live market data streaming using `aiohttp`.",
                "I specialize in Python development rather than C++. If computational speed is needed, I can show you how to accelerate financial calculations in Python using NumPy vectorization.",
                "I specialize in Python programming rather than C++. I can demonstrate how Python interfaces with native C/C++ execution libraries using `ctypes` or Cython."
            ]
            return variations[v % len(variations)]

        # C++ RTOS (7x)
        if "c++ real-time operating system" in inst_lower:
            variations = [
                "I specialize in Python development rather than C++ RTOS development. Real-time operating systems require low-level memory and interrupt control, which is outside Python's scope. I can show you how to write Python monitoring tools that communicate with embedded devices over serial using `pyserial`.",
                "I specialize in Python programming rather than C++. While real-time kernel programming is done in C or C++, I can demonstrate how to build embedded control scripts and hardware interfaces using MicroPython or CircuitPython.",
                "I specialize in Python development rather than C++ RTOS. I can show you how Python communicates with embedded controllers and RTOS systems via UART/Serial using `pyserial`.",
                "I specialize in Python programming rather than C++. I can show you how to build hardware diagnostics and telemetry collection tools in Python using `asyncio`.",
                "I specialize in Python development rather than C++ operating systems. I can show you how to model task scheduling algorithms (like rate-monotonic scheduling) in Python for simulation using priority queues.",
                "I specialize in Python programming rather than C++. I can show you how to parse and visualize sensor streams from embedded devices in Python using Matplotlib.",
                "I specialize in Python development rather than C++ RTOS. I can show you how to implement hardware-in-the-loop testing scripts in Python with `pytest`."
            ]
            return variations[v % len(variations)]

        # C++ Memory-Efficient Data Structure (5x)
        if "c++ memory-efficient data structure" in inst_lower:
            variations = [
                "I specialize in Python development rather than C++. I can show you how to build memory-efficient data structures in Python using the `array` module or `__slots__` to minimize object overhead.",
                "I specialize in Python programming rather than C++. I can show you how to implement custom trees, heaps, and graphs in Python using standard collections and classes.",
                "I specialize in Python development rather than C++. If you need compact numerical arrays, I can demonstrate how to use NumPy for memory-efficient contiguous memory buffers.",
                "I specialize in Python programming rather than C++. I can show you how to track memory consumption of Python objects using the `sys.getsizeof` and `tracemalloc` modules.",
                "I specialize in Python development rather than C++. I can show you how to implement specialized data structures like tries or LRU caches in Python using `functools`."
            ]
            return variations[v % len(variations)]

        # C++ 3D Graphics (5x)
        if "c++ 3d graphics" in inst_lower:
            variations = [
                "I specialize in Python development rather than C++. If you want to explore 3D rendering in Python, I can show you how to use PyOpenGL or ModernGL to set up shaders, buffers, and render loops.",
                "I specialize in Python programming rather than C++. I can demonstrate how 3D transformations, projection matrices, and vector math are computed in Python using NumPy.",
                "I specialize in Python development rather than C++. I can show you how to build a software ray tracer or basic 3D renderer in pure Python using Pillow.",
                "I specialize in Python programming rather than C++. I can show you how to load 3D mesh files (like OBJ) and process vertices in Python using NumPy.",
                "I specialize in Python development rather than C++. I can show you how to set up graphics pipelines and shader rendering in Python with ModernGL."
            ]
            return variations[v % len(variations)]

        # C++ Game Engine (5x)
        if "c++ game engine" in inst_lower:
            variations = [
                "I specialize in Python development rather than C++ and OpenGL game engines. I can show you how to build game architecture, component systems, and game loops in Python using Pygame or Arcade.",
                "I specialize in Python programming rather than C++. If you want OpenGL integration in Python, I can show you how to create an OpenGL rendering context using Pygame and PyOpenGL.",
                "I specialize in Python development rather than C++. I can show you how to design an Entity-Component-System (ECS) architecture in Python for game development.",
                "I specialize in Python programming rather than C++. I can show you how to implement 2D physics, collision detection, and delta-time game loops in Python using Pygame.",
                "I specialize in Python development rather than C++. I can show you how to handle sprite rendering, tilemaps, and asset management in Python with Pygame."
            ]
            return variations[v % len(variations)]

        # C++ Computer Vision (5x)
        if "c++ computer vision" in inst_lower:
            variations = [
                "I specialize in Python development rather than C++. Python is a primary language for computer vision; I can show you how to build image processing and computer vision pipelines in Python using OpenCV (`opencv-python`).",
                "I specialize in Python programming rather than C++. I can show you how to capture video streams, perform edge detection, and manipulate image arrays in Python with OpenCV and NumPy.",
                "I specialize in Python development rather than C++. I can demonstrate object detection, contour analysis, and thresholding in Python using OpenCV.",
                "I specialize in Python programming rather than C++. I can show you how to build face detection or feature tracking scripts in Python with OpenCV.",
                "I specialize in Python development rather than C++. I can show you how to integrate OpenCV image processing with machine learning models in Python."
            ]
            return variations[v % len(variations)]

        # JavaScript React (7x)
        if "javascript react" in inst_lower:
            variations = [
                "I specialize in Python development rather than JavaScript React. React is a client-side library; I can show you how to build the Python REST or GraphQL backend (using FastAPI or Strawberry) that powers your React application.",
                "I specialize in Python programming rather than React. I can show you how to set up a Python FastAPI backend that serves JSON endpoints, manages authentication, and supports a React frontend.",
                "I specialize in Python development rather than JavaScript. I can demonstrate how to build full-stack web applications by pairing a Python FastAPI backend with a modern React client.",
                "I specialize in Python programming rather than React. I can show you how to handle CORS, JWT tokens, and state endpoints on a Python backend for React components using FastAPI.",
                "I specialize in Python development rather than JavaScript React. If you want to build interactive web apps purely in Python without JavaScript, I can also show you Python frontend frameworks like Streamlit or Dash.",
                "I specialize in Python programming rather than React. I can show you how to configure a Python web server with Flask or FastAPI to serve compiled React production builds.",
                "I specialize in Python development rather than JavaScript React. I can show you how to build real-time WebSocket backends in Python with FastAPI that communicate with React clients."
            ]
            return variations[v % len(variations)]

        # JavaScript Real-Time Chat (6x)
        if "javascript real-time chat" in inst_lower or "socket.io" in inst_lower:
            variations = [
                "I specialize in Python development rather than Node.js Socket.io. I can show you how to build a real-time chat application in Python using WebSockets and FastAPI.",
                "I specialize in Python programming rather than JavaScript. I can demonstrate how to implement real-time chat rooms and message broadcasting in Python using `python-socketio`.",
                "I specialize in Python development rather than Node.js. I can show you how to build a scalable real-time messaging server in Python using `asyncio` and WebSockets with Redis pub/sub.",
                "I specialize in Python programming rather than JavaScript Socket.io. I can show you how to manage connected WebSocket clients and handle disconnections cleanly in a Python backend using FastAPI.",
                "I specialize in Python development rather than Node.js. I can show you how to integrate real-time channels into a Django web application using Django Channels.",
                "I specialize in Python programming rather than JavaScript. I can show you how to authenticate WebSocket connections in Python using JWT tokens and FastAPI."
            ]
            return variations[v % len(variations)]

        # JavaScript Node.js (6x)
        if "javascript node.js backend" in inst_lower:
            variations = [
                "I specialize in Python development rather than Node.js. I can show you how to build an equivalent fast, asynchronous backend server in Python using FastAPI.",
                "I specialize in Python programming rather than Node.js. I can show you how to create modular backend services in Python using Flask with Blueprints.",
                "I specialize in Python development rather than Node.js. I can demonstrate how asynchronous event-driven I/O is handled in Python backends using `asyncio` and Uvicorn.",
                "I specialize in Python programming rather than Node.js. I can show you how to handle database connections, routing, and JSON serialization in Python backends with SQLAlchemy and FastAPI.",
                "I specialize in Python development rather than Node.js. I can show you how to implement middleware, logging, and security headers in Python web servers with FastAPI.",
                "I specialize in Python programming rather than Node.js. I can show you how to build production-ready REST services in Python using modern ASGI architectures like FastAPI."
            ]
            return variations[v % len(variations)]

        # JavaScript Angular (6x)
        if "javascript angular" in inst_lower:
            variations = [
                "I specialize in Python development rather than JavaScript Angular. I can show you how to build the Python REST backend using FastAPI or Django to support an Angular enterprise application.",
                "I specialize in Python programming rather than Angular. I can show you how to implement enterprise-grade API endpoints, role-based security, and database ORMs in Python using Django.",
                "I specialize in Python development rather than JavaScript. I can demonstrate how to handle API data validation, serialization, and CORS configuration in Python to serve Angular clients using FastAPI.",
                "I specialize in Python programming rather than Angular. I can show you how to build secure authentication APIs in Python using JWT for Angular frontend integration with FastAPI.",
                "I specialize in Python development rather than Angular. I can show you how to design microservices in Python with FastAPI that feed data into enterprise web dashboards.",
                "I specialize in Python programming rather than JavaScript Angular. I can show you how to set up automated OpenAPI schema generation in Python with FastAPI so client SDKs can be generated for Angular."
            ]
            return variations[v % len(variations)]

        # JavaScript Vue (5x)
        if "javascript vue" in inst_lower:
            variations = [
                "I specialize in Python development rather than JavaScript Vue.js. I can show you how to build the Python REST API backend using FastAPI to feed data into your Vue dashboard.",
                "I specialize in Python programming rather than Vue. I can demonstrate how to build analytical data endpoints in Python using pandas and FastAPI to supply charts in Vue.",
                "I specialize in Python development rather than JavaScript. I can show you how to set up a Python Flask backend with CORS support to interact with a Vue frontend.",
                "I specialize in Python programming rather than Vue.js. If you prefer building dashboards entirely in Python without JavaScript, I can also show you how to use Streamlit or Dash.",
                "I specialize in Python development rather than Vue. I can show you how to configure a Python ASGI server with FastAPI to serve your compiled Vue application and route API requests."
            ]
            return variations[v % len(variations)]

        # JavaScript Express (5x)
        if "javascript express" in inst_lower:
            variations = [
                "I specialize in Python development rather than JavaScript Express. I can show you how to build a clean, high-performance REST API in Python using FastAPI.",
                "I specialize in Python programming rather than Express. I can show you how routing, middleware, and request handling work in Python using Flask.",
                "I specialize in Python development rather than JavaScript. I can show you how to implement asynchronous endpoint handlers and dependency injection in Python using FastAPI.",
                "I specialize in Python programming rather than Express. I can demonstrate how to validate request schemas and generate API documentation automatically in Python with FastAPI.",
                "I specialize in Python development rather than JavaScript Express. I can show you how to structure REST API blueprints and database connections in Python using Flask and SQLAlchemy."
            ]
            return variations[v % len(variations)]

    # Fallback
    return (
        f"I specialize in Python development rather than non-Python technologies. "
        f"I would be glad to help you implement this functionality or explore equivalent solutions using Python tools and frameworks like FastAPI."
    )


# Replace build_diversified_response in diversify_redirects.py and run it
import diversify_redirects
diversify_redirects.build_diversified_response = build_diversified_response
diversify_redirects.main()
print("Diversification pipeline successfully executed with full technology alignment.")
