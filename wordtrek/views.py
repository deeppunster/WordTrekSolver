from django.shortcuts import render

# Create your views here.



class QuestionAdmin(admin.ModelAdmin):
    """
    Create a model for the admin pages.
    """
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']})
        ]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    inlines = [ChoiceInLine]
    list_filter = ['pub_date']
    search_fields = ['question_text']
