LITReview = {
    models = {
        Ticket = {
            title = "CharField(max_length=128)",
            description = "TextField(max_length=2048, blank=True)",
            user = "ForeignKey(User, on_delete=models.CASCADE)",
            image = "ImageField(null=True, blank=True)",
            time_created = "DateTimeField(auto_now_add=True)"
        },
        Review = {
            ticket = "ForeignKey(Ticket, on_delete=models.CASCADE)",
            rating = "PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])",
            user = "ForeignKey(User, on_delete=models.CASCADE)",
            headline = "CharField(max_length=128)",
            body = "TextField(max_length=8192, blank=True)",
            time_created = "DateTimeField(auto_now_add=True)"
        },
        UserFollows = {
            user = "ForeignKey(User, related_name='following', on_delete=models.CASCADE)",
            followed_user = "ForeignKey(User, related_name='followed_by', on_delete=models.CASCADE)",
            meta = "unique_together = ('user', 'followed_user')"
        }
    },
    
    views = {
        TicketCreateView = {
            model = "Ticket",
            fields = "{'title', 'description', 'image'}",
            template_name = "reviews/ticket_form.html",
            success_url = "'/'"
        },
        ReviewCreateView = {
            model = "Review",
            fields = "{'ticket', 'rating', 'headline', 'body'}",
            template_name = "reviews/review_form.html",
            success_url = "'/'"
        },
        TicketListView = {
            model = "Ticket",
            template_name = "reviews/ticket_list.html",
            context_object_name = "'tickets'"
        },
        ReviewListView = {
            model = "Review",
            template_name = "reviews/review_list.html",
            context_object_name = "'reviews'"
        },
        UserFollowsCreateView = {
            model = "UserFollows",
            fields = "{'followed_user'}",
            template_name = "reviews/userfollows_form.html",
            success_url = "'/'"
        },
        UserFollowsListView = {
            model = "UserFollows",
            template_name = "reviews/userfollows_list.html",
            context_object_name = "'follows'"
        },
        UserFollowsDeleteView = {
            model = "UserFollows",
            success_url = "'/'"
        }
    },
    
    urls = {
        path("tickets/create/", "TicketCreateView.as_view(), name='ticket-create'"),
        path("reviews/create/", "ReviewCreateView.as_view(), name='review-create'"),
        path("tickets/", "TicketListView.as_view(), name='ticket-list'"),
        path("reviews/", "ReviewListView.as_view(), name='review-list'"),
        path("follows/create/", "UserFollowsCreateView.as_view(), name='follow-create'"),
        path("follows/", "UserFollowsListView.as_view(), name='follow-list'"),
        path("follows/delete/<int:pk>/", "UserFollowsDeleteView.as_view(), name='follow-delete'")
    },

    templates = {
        ticket_form_html = [[
        {% extends "base_generic.html" %}

        {% block content %}
        <div class="container">
            <h2>Créer un nouveau ticket</h2>
            <form method="post" enctype="multipart/form-data">
                {% csrf_token %}
                {{ form.as_p }}
                <button type="submit" class="btn btn-primary">Enregistrer</button>
            </form>
        </div>
        {% endblock %}
        ]],
        
        ticket_list_html = [[
        {% extends "base_generic.html" %}

        {% block content %}
        <div class="container">
            <h2>Liste des Tickets</h2>
            <ul>
                {% for ticket in tickets %}
                <li>{{ ticket.title }} - {{ ticket.user.username }}</li>
                {% endfor %}
            </ul>
        </div>
        {% endblock %}
        ]]
    }
}
