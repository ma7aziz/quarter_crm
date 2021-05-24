# A stream implementation using an in-memory bytes buffer
from io import BytesIO, StringIO
# It inherits BufferIOBase

from django.http import HttpResponse
from django.template.loader import get_template

# pisa is a html2pdf converter using the ReportLab Toolkit,
# the HTML5lib and pyPdf.

from xhtml2pdf import pisa
# difine render_to_pdf() function

import io


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()

    # This part will create the pdf.
    # pdf = pisa.pisaDocument(
    #     BytesIO(html.encode("utf-8")), result, encoding="utf-8")
    pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
