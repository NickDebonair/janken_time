from django import template

register = template.Library() # Djangoのテンプレートタグライブラリ

# カスタムタグとして登録する
@register.simple_tag
def paginated_plus(value1, value2):
    return value1 + (value2-1)*7