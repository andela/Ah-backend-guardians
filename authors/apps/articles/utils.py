def get_likes_or_dislikes(**kwargs):
    likes = kwargs.get('model').objects.all().filter(
        article_like=kwargs.get('like_article')
    )
    filtered_likes = likes.filter(article_id=kwargs.get('article_id'))
    return filtered_likes.count()
