from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from events.models import Event, User
from datetime import datetime

from events.forms import CreateForm
from users.forms import UserForm, RegisterForm


# Create your views here.
class Index(View): 
    template_name = "events/index.html"

    def get(self, request): 
        user_form = UserForm()
        create_form = CreateForm()
        register_form = RegisterForm()

        context = {
            'user_form': user_form,
            "create_form": create_form,
            "register_form": register_form,
            }
        return render(request, self.template_name, context)


class Create(View):
    def post(self, request):
        if request.is_ajax():
            content = request.POST
        else:
            body = request.body.decode()
            if not body: 
                return JsonResponse ({"response":"Missing Body"})
            content = json.loads(body)

        title = content.get("title")
        description = content.get("description")
        location = content.get("location")
        date = content.get("date")
        token = content.get("token")

        date_obj = datetime.strptime(date, '%m/%d/%Y %I:%M %p')
        user = User.objects.get(access_token = token)
        event = Event.objects.create(title=title, description=description, location=location, date=date_obj, creator=user)
        res = event.to_json()

        if event:
            return JsonResponse({"response": "Added Event!",'events': res})
        else:
            return JsonResponse ({"response":"Invalid information"})


class All(View):
    def post(self, request):
        if request.is_ajax():
            content = request.POST
        else:
            body = request.body.decode()
            if not body: 
                return JsonResponse ({"response":"Missing Body"})
            content = json.loads(body)

        token = content.get("token")
        user = User.objects.get(access_token=token)
        events = Event.objects.filter(creator=user)
        
        res = [event.to_json() for event in events]
        if res:
            return JsonResponse({"Message": "you have events", "events": res})
        else:
            return JsonResponse ({"response":"Invalid information"})


class Edit(View):
    template = "events/index.html"

    def get(self, request, pk=None):
        # get the slug id from the object
        event = Event.objects.get(pk=pk)
        # get the form and populate it with the value that is already there, AKA what we want ot edit
        form = CreateForm(instance=event)
        context = {
            "event_id": event.id,
            "edit_form": form.as_p(),}
        return JsonResponse(context)

    def post(self, request, pk):
        pass
        if request.is_ajax():
            content = request.POST
        else:
            body = request.body.decode()
            if not body: 
                return JsonResponse ({"response":"Missing Body"})
            content = json.loads(body)

        pk = pk
        token = content.get("token")
        title = content.get("title")
        description = content.get("description")
        location = content.get("location")
        date = content.get("date")

        # date_obj = datetime.strptime(date, '%m/%d/%Y %I:%M %p')
        user = User.objects.get(access_token = token)
        event = user.author.filter(pk=pk)
        if not event:
            return JsonResponse ({"response":"Invalid information"}, status=404)
        
        # use index 0 becuase we use filter to get the event
        event_form = CreateForm(data=content,instance=event[0])
        if event_form.is_valid():
            event = event_form.save()
            res = event.to_json()
            return JsonResponse({"Message": "Update succesfull", "events": res})
        else:
            return JsonResponse ({"response":"Invalid information","errors":event_form.errors}, status=406)


class Delete(View):
    def post(self, request, pk):
        if request.is_ajax():
            content = request.POST
        else:
            body = request.body.decode()
            if not body: 
                return JsonResponse ({"response":"Missing Body"})
            content = json.loads(body)

        token = content.get("token")
        pk = pk

        user = User.objects.get(access_token = token)
        event = Event.objects.get(pk = pk, creator=user)
        event.delete()
        if event:
            return JsonResponse({"Deleted": "True"})
        else:
            return JsonResponse ({"response":"Invalid information"})


class Attend(View):
    def post(self, request, pk):
        if request.is_ajax():
            content = request.POST
        else:
            body = request.body.decode()
            if not body: 
                return JsonResponse ({"response":"Missing Body"})
            content = json.loads(body)

        token = content.get("token")
        pk = pk

        user = User.objects.get(access_token = token)
        event = Event.objects.get(pk = pk)

        event.attending.add(user)
        
        event.save()

        if event:
            return JsonResponse({"Attending": "True"})
        else:
            return JsonResponse ({"response":"Invalid information"})


class GetAll(View):
    def post(self, request):
        if request.is_ajax():
            content = request.POST
        else:
            body = request.body.decode()
            if not body: 
                return JsonResponse ({"response":"Missing Body"})
            content = json.loads(body)

        events = Event.objects.filter()
        res = [event.to_json() for event in events]
        if res:
            return JsonResponse({"events": res})
        else:
            return JsonResponse ({"response":"Invalid information"})


class Attending(View):
    def post(self, request):
        if request.is_ajax():
            content = request.POST
        else:
            body = request.body.decode()
            if not body: 
                return JsonResponse ({"response":"Missing Body"})
            content = json.loads(body)

        token = content.get("token")
        user = User.objects.get(access_token = token)
        events = Event.objects.filter(attending=user)

        res = [event.to_json() for event in events]
        if res:
            return JsonResponse({"events": res})
        else:
            return JsonResponse ({"response":"Invalid information"})




