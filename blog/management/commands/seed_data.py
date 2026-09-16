from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Category, Tag, Post, Comment, Profile

class Command(BaseCommand):
    help = 'Seeds database with initial superuser, demo authors, categories, tags, posts, and comments'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding database..."))

        # 1. Create Admin User
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@devpulse.io',
                'first_name': 'System',
                'last_name': 'Administrator',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            admin_user.profile.bio = "System Administrator and lead editor at DevPulse."
            admin_user.profile.location = "San Francisco, CA"
            admin_user.profile.save()
            self.stdout.write(self.style.SUCCESS("Superuser created: admin / admin123"))
        else:
            self.stdout.write("Superuser 'admin' already exists.")

        # 2. Create Demo Authors
        authors_data = [
            {'username': 'alex_dev', 'email': 'alex@devpulse.io', 'first_name': 'Alex', 'last_name': 'Rivers', 'bio': 'Senior Backend Engineer specializing in Python, Django, and distributed systems.'},
            {'username': 'sarah_arch', 'email': 'sarah@devpulse.io', 'first_name': 'Sarah', 'last_name': 'Chen', 'bio': 'Cloud Architect passionate about microservices, Kubernetes, and DevOps.'},
            {'username': 'david_ui', 'email': 'david@devpulse.io', 'first_name': 'David', 'last_name': 'Kovac', 'bio': 'Frontend developer and UI designer creating seamless web experiences.'},
        ]

        authors = [admin_user]
        for adata in authors_data:
            user, created = User.objects.get_or_create(
                username=adata['username'],
                defaults={
                    'email': adata['email'],
                    'first_name': adata['first_name'],
                    'last_name': adata['last_name'],
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                user.profile.bio = adata['bio']
                user.profile.save()
            authors.append(user)
        
        self.stdout.write(self.style.SUCCESS(f"Demo users ready: {[a.username for a in authors]}"))

        # 3. Create Categories
        cat_data = [
            ('Web Development', 'Articles on backend and frontend web technologies, frameworks, and APIs.'),
            ('Cloud & DevOps', 'Infrastructure as Code, Docker, Kubernetes, CI/CD pipelines, and cloud hosting.'),
            ('Software Architecture', 'Design patterns, system architecture, database optimization, and performance.'),
            ('Artificial Intelligence', 'Machine learning engineering, LLM integration, and AI-powered app design.'),
        ]
        categories = {}
        for cname, cdesc in cat_data:
            cat, _ = Category.objects.get_or_create(name=cname, defaults={'description': cdesc})
            categories[cname] = cat
        self.stdout.write(self.style.SUCCESS(f"Categories seeded: {list(categories.keys())}"))

        # 4. Create Tags
        tag_names = ['Python', 'Django', 'PostgreSQL', 'Docker', 'REST API', 'System Design', 'JavaScript', 'Tailwind']
        tags = {}
        for tname in tag_names:
            tag, _ = Tag.objects.get_or_create(name=tname)
            tags[tname] = tag

        # 5. Create Sample Blog Posts
        posts_seed = [
            {
                'title': 'Building Scalable Web Applications with Django 5 and PostgreSQL',
                'author': authors[1], # alex_dev
                'category': categories['Web Development'],
                'tags_list': [tags['Python'], tags['Django'], tags['PostgreSQL']],
                'status': 'published',
                'featured_image': 'posts/post_1.jpg',
                'content': '''<p>Building high-performance, scalable web applications requires a solid architectural foundation. In Django 5, several new features streamline async handling, database connection pooling, and ORM optimizations.</p>
<h3>1. Database Connection Pooling</h3>
<p>When running high-throughput Django servers, establishing database connections on every request creates latency. Utilizing built-in connection pooling or external tools like <strong>PgBouncer</strong> keeps connection overhead minimal.</p>
<h3>2. Query Optimization</h3>
<p>Always avoid N+1 queries by leveraging <code>select_related()</code> for ForeignKey joins and <code>prefetch_related()</code> for ManyToMany relationships.</p>
<pre><code># Optimized query example
posts = Post.objects.filter(status='published')\\
                    .select_related('author', 'category')\\
                    .prefetch_related('tags')
</code></pre>
<p>By implementing proper caching with Redis and optimizing indexing, Django applications comfortably scale to millions of monthly active users.</p>'''
            },
            {
                'title': 'Containerizing Python Applications with Multi-Stage Docker Builds',
                'author': authors[2], # sarah_arch
                'category': categories['Cloud & DevOps'],
                'tags_list': [tags['Docker'], tags['Python'], tags['System Design']],
                'status': 'published',
                'featured_image': 'posts/post_2.jpg',
                'content': '''<p>Docker containerization is standard practice for modern deployment, but naive Dockerfiles often yield bloated image sizes exceeding 1 GB.</p>
<h3>Why Multi-Stage Builds Matter</h3>
<p>Multi-stage builds allow you to compile dependencies in an interim build container and copy only the final artifacts into a slim runtime container (such as <code>python:3.11-slim</code> or Alpine Linux).</p>
<p>This drastically reduces security vulnerability exposure and speeds up container deployment in production clusters.</p>'''
            },
            {
                'title': 'Designing Resilient Microservices & Event-Driven Systems',
                'author': authors[0], # admin
                'category': categories['Software Architecture'],
                'tags_list': [tags['System Design'], tags['REST API']],
                'status': 'published',
                'featured_image': 'posts/post_3.jpg',
                'content': '''<p>Monolithic applications are simple to develop initially, but as teams grow, decoupling into event-driven microservices provides team autonomy and independent deployment pipelines.</p>
<p>Key patterns discussed include:</p>
<ul>
  <li><strong>Circuit Breakers</strong> to prevent cascading service failures</li>
  <li><strong>Event Sourcing</strong> for auditability and real-time event streaming</li>
  <li><strong>Idempotency Keys</strong> in API payloads to prevent duplicate mutations</li>
</ul>'''
            },
            {
                'title': 'Draft: Integrating Large Language Models with Django Background Tasks',
                'author': authors[1], # alex_dev
                'category': categories['Artificial Intelligence'],
                'tags_list': [tags['Python'], tags['Django']],
                'status': 'draft',
                'featured_image': 'posts/post_4.jpg',
                'content': '''<p>Work in progress draft on offloading heavy LLM inference and API calls to Celery or Redis Queue workers...</p>'''
            },
            {
                'title': 'The Rise of Agentic AI: From Passive Prompts to Autonomous Action',
                'author': authors[1], # alex_dev
                'category': categories['Artificial Intelligence'],
                'tags_list': [tags['Python'], tags['System Design']],
                'status': 'published',
                'featured_image': 'posts/post_5.jpg',
                'content': '''<p>Agentic AI represents a paradigm shift from simple chatbot Q&A to autonomous systems capable of planning, tool invocation, self-correction, and multi-step execution.</p>'''
            }
        ]

        for pdata in posts_seed:
            post, pcreated = Post.objects.get_or_create(
                title=pdata['title'],
                defaults={
                    'author': pdata['author'],
                    'category': pdata['category'],
                    'status': pdata['status'],
                    'featured_image': pdata.get('featured_image', ''),
                    'content': pdata['content'],
                    'views_count': 42
                }
            )
            if pcreated:
                post.tags.set(pdata['tags_list'])
                post.likes.add(authors[0], authors[2])
                self.stdout.write(self.style.SUCCESS(f"Post created: '{post.title}'"))

                # Add sample comments
                c1 = Comment.objects.create(
                    post=post,
                    author=authors[2],
                    content="Fantastic article! Connection pooling transformed our response latency significantly."
                )
                Comment.objects.create(
                    post=post,
                    author=pdata['author'],
                    parent=c1,
                    content="Glad to hear that! Make sure to tune your max_connections setting on PostgreSQL as well."
                )

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
