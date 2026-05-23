from django.urls import path
from .views.ocr_views import test_api
from .views.ocr_views import ocr_function
from .views.llm_views import llm_function
from .views.keyword_views import keyword_function
from .views.learning_views import learning_function
from api.views.media_create_views import (MediaEpisodeCreateView)
from api.views.wordbook_list_view import (WordBookListView)
from api.views.wordbook_wordcard_list_view import (WordBookWordCardListView)
from api.views.google_login_views import GoogleLoginView
from api.views.episode_list_view import (EpisodeListView)
from api.views.wordbook_auto_create_view import (WordBookAutoCreateView)
from api.views.wordbook_episode_add_view import (WordBookEpisodeAddView)
from api.views.wordbook_episode_delete_view import (WordBookEpisodeDeleteView)
from api.views.wordbook_episode_update_view import (WordBookEpisodeUpdateView)
from api.views.wordbook_delete_view import (WordBookDeleteView)
from api.views.wordbook_name_update_view import (WordBookNameUpdateView)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api.views.wordcard_learned_update_view import (
    WordCardLearnedUpdateView
)
urlpatterns = [
    path('upload-image/', ocr_function),
    path('llm/', llm_function),
    path('word-pick/', keyword_function),
    path('generate-learning/', learning_function),
    path("medias/", MediaEpisodeCreateView.as_view()),
    path("login/", GoogleLoginView.as_view()),
    path("wordbooks/", WordBookListView.as_view()),
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("wordbooks/<int:word_book_id>/wordcards/", WordBookWordCardListView.as_view()),
    path("episodes/",EpisodeListView.as_view()),
    path("wordbooks/<int:word_book_id>/episodes/", WordBookEpisodeAddView.as_view()),
    path("wordbooks/<int:word_book_id>/episodes/<int:episode_id>/", WordBookEpisodeDeleteView.as_view()),
    path("wordcards/<int:wordcard_id>/", WordCardLearnedUpdateView.as_view()), 
    path("wordbooks/<int:word_book_id>/episodes/", WordBookEpisodeUpdateView.as_view()),
    path("wordbooks/<int:word_book_id>/", WordBookDeleteView.as_view()),
    path("wordbooks/<int:word_book_id>/", WordBookNameUpdateView.as_view()),
]