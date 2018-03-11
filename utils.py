from django.urls import reverse


def nav_context(request):
    nav_items = [(reverse("messages:list_public"), "Public messages")]
    if request.user.is_authenticated:
        if request.user.is_politician:
            nav_items.append((reverse("messages:statistics"), "Statistics"))
            nav_items.append((reverse("users:filterers"), "Your filterers"))
        else:
            nav_items.append((reverse("messages:new"), "Send message"))
            nav_items.append((reverse("messages:sent_by_me"), "Messages you've sent"))
            if request.user.is_normal_user:
                pass
            elif request.user.is_filterer:
                nav_items.append((reverse("users:politicians"), "Politicians"))
        nav_items.append((reverse("auth:logout"), "Logout"))
    else:
        nav_items.extend([(reverse("auth:login"), "Login"), (reverse("auth:signup"), "Sign Up")])
    return {"nav_items": nav_items}
