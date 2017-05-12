

# this is the content of the HTML file which might be better
# used as a simple open.read but we need to put in the bs4....

SRC_HTML = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">

<html>
<head>
<title>Test Source HTML</title>
<style type="text/css">
a, body, div, span, td {font-family:Lucida Sans Unicode,Arial Unicode MS,Lucida Sans,Helvetica,Arial,sans-serif}
</style>
</head>
<body>
<div id="A">
<h2>A</h2>
<p>All nouns beginning with <span lang="HAW">a-</span> or <span lang="HAW">ā-</span> may be preceded by the article <span lang="HAW">ke</span>. Nouns beginning with <span lang="HAW">ʻa-</span> or <span lang="HAW">ʻā-</span> may be preceded by the article <span lang="HAW">ka</span>, unless otherwise stated.</p>
<div id="A.1">
<span lang="HAW">a </span>
<p><span>1.</span> <span>prep.</span> Of, acquired by. This <span lang="HAW">a</span> forms part of the possessives, as in <span lang="HAW">ka'u</span>, mine, and <span lang="HAW">kāna</span>, his. (<span>Gram. 9.6.1</span>.)<span lang="HAW">ʻUmi-a-Līloa</span>, <span lang="ENG"><span lang="HAW">ʻUmi</span>, [son] of <span lang="HAW">Līloa</span></span>. <span lang="HAW">Hale-a-ka-lā</span>, <span lang="ENG">house acquired [or used] by the sun [mountain name]</span>. (PPN <span lang="HAW">ʻa</span>.)</p>
<p><span>2.</span> <em>(Cap.)</em> <span>nvs.</span> Abbreviation of <span lang="HAW">ʻākau</span>, north, as in surveying reports.</p>
</div>
<div id="A.2">
<span lang="HAW">-a </span>
<p>Pas/imp. suffix. (<span>Gram. 6.6.3</span>.) (PPN <span lang="HAW">-a</span>.)</p>
</div>
<div id="A.15">
<span lang="HAW">ʻaʻa.ʻā </span>
<p><span>1.</span> Redup. of <span lang="HAW">ʻaʻā</span> 1; lava cave.</p>
<p><span>2.</span> Redup. of <span lang="HAW">ʻāʻā</span> 1.</p>
</div>
<div id="A.18">
<span lang="HAW">ʻaʻa.ahi </span>
<p><span>n.</span> Bag for carrying fire-making equipment (<span lang="HAW">ʻaʻa</span>, <span lang="ENG">bag</span>, and <span lang="HAW">ahi</span>, <span lang="ENG">fire</span>).</p>
</div>
</div>
</body>
</html>
"""

SRC_TEXT = """


Test Source HTML

a, body, div, span, td {font-family:Lucida Sans Unicode,Arial Unicode MS,Lucida Sans,Helvetica,Arial,sans-serif}




A
All nouns beginning with a- or ā- may be preceded by the article ke. Nouns beginning with ʻa- or ʻā- may be preceded by the article ka, unless otherwise stated.

a 
1. prep. Of, acquired by. This a forms part of the possessives, as in ka'u, mine, and kāna, his. (Gram. 9.6.1.)ʻUmi-a-Līloa, ʻUmi, [son] of Līloa. Hale-a-ka-lā, house acquired [or used] by the sun [mountain name]. (PPN ʻa.)
2. (Cap.) nvs. Abbreviation of ʻākau, north, as in surveying reports.


-a 
Pas/imp. suffix. (Gram. 6.6.3.) (PPN -a.)


ʻaʻa.ʻā 
1. Redup. of ʻaʻā 1; lava cave.
2. Redup. of ʻāʻā 1.


ʻaʻa.ahi 
n. Bag for carrying fire-making equipment (ʻaʻa, bag, and ahi, fire).




"""