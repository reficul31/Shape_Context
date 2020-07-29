import os
from lxml import etree
import matplotlib.pyplot as plt
import base64
import io

def mathml2latex_yarosh(equation):
    """ MathML to LaTeX conversion with XSLT from Vasil Yaroshevich """
    xslt_file = os.path.join('xsl_yarosh', 'mmltex.xsl')
    dom = etree.fromstring(equation)
    xslt = etree.parse(xslt_file)
    transform = etree.XSLT(xslt)
    newdom = transform(dom)
    return newdom

mathml = """


<math display='block'><mrow><mrow><msub><mo>&#x222b;</mo><mrow><mi>D</mi></mrow></msub><mrow><mo>(</mo><mo>&#x2207;&#x22c5;</mo><mi>F</mi><mo>)</mo></mrow><mi>d</mi><mrow><mi>V</mi></mrow></mrow><mo>=</mo><mrow><msub><mo>&#x222b;</mo><mrow><mo>&#x2202;</mo><mi>D</mi></mrow></msub><mrow><mtext>&#x2009;</mtext><mi>F</mi><mo>&#x22c5;</mo><mi>n</mi></mrow><mi>d</mi><mi>S</mi></mrow></mrow></math>"""
tex = mathml2latex_yarosh(mathml)
print(tex)                                                         

fig, ax = plt.subplots()

fig.patch.set_visible(False)
ax.axis('off')
ax.text(0, 0.6, tex, fontsize = 50)                                  

io_bytes = io.BytesIO()
plt.savefig(io_bytes,  format='png')
io_bytes.seek(0)
img_string = base64.b64encode(io_bytes.read())
print(img_string)