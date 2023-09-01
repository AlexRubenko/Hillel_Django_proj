from django.db.models import Q
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from webargs import fields
from webargs.djangoparser import use_args

from document_flow.models import CADDocument


def index(request):
    return render(request, 'document_flow/index.html')


@use_args(
    {
        "document_number": fields.Str(
            required=False,
        ),
        "document_name": fields.Str(
            required=False,
        ),
        "search": fields.Str(
            required=False,
        ),
    },
    location="query"
)
def get_documents(request, params):
    print(params)
    documents = CADDocument.objects.all()

    search_fields = ["document_number", "document_name"]

    for param_name, param_value in params.items():
        if param_name == "search":
            or_filter = Q()
            for field in search_fields:
                or_filter |= Q(**{F"{field}__icontains": param_value})
            documents = documents.filter(or_filter)
        else:
            documents = documents.filter(**{param_name: param_value})

    return render(request,
                  template_name="document_flow/documents_list.html",
                  context={"documents": documents})


@csrf_exempt
def update_document(request, pk):
    pass


@csrf_exempt
def delete_document(request, pk):
    pass


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)
