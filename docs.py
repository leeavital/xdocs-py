"""
This is a program to transform xml into pretty documentation
written in a heavily object-oriented style
"""

print "initialzing doc tool..."


from xml.dom.minidom import parseString
import xml.dom


odir = ""




class Config:
	stylesheet = "style.css"



class InputReader:
	"""This abstract class reads input--subclasses can read input from a file or directly from a string or perhaps from a URL"""
	
	__slots__ = ("docParser")

	def getParser(self):
		return self.docParser

class InFileReader(InputReader):
	"""class used to generate the documents from an infilename.
		extends InputReader
	"""

	__slots__ = ("infilename", "docParser")

	def __init__(self, infilename):
		self.infilename = infilename
		xmls = open(self.infilename).read()
		self.docParser = DocParser(xmls)



class DocParser:
	"""class used to read an xml document"""

	__slots__ = ("modules")

	def __init__(self, doc):
		"""reads tre structure of the xml document
			doc : a string that contains an xml document"""
		self.doc = doc
		self.modules = []

		dom = parseString(doc)

		root = dom.getElementsByTagName("project")[0]
		for rootMod in root.childNodes:
			r = ModuleFactory.makeModule(rootMod)
			if isinstance(r, Module):
				self.modules.append(r)

	def getModules(self):
		"""get the root modules"""
		return self.modules


class Module:
	"""abstract class to represent a documentation  module"""
	
	__slots__ = ("children", "level")

	def getHTML(self):
		return "no html for abstract modules"


	
	
	def __init__(self, elm, level=0):
		self.children = []
		self.level = 0
		for child in elm.childNodes:
			self.children.append( ModuleFactory.makeModule(child) )


class ModuleFactory:
	"""factory class for modules"""

	@staticmethod
	def makeModule(elm):
		
		if isinstance(elm, xml.dom.Node) and elm.nodeType == elm.ELEMENT_NODE:

			if elm.tagName == "package":
				return PackageModule(elm)
			elif elm.tagName == "class":
				return ClassModule(elm)
			else:
				print "error: unknown tag name -- %s" % elm.tagName
		

class PackageModule(Module):

	__slots__ = ("name", "description")

	def __init__(self, elm, level=0):
		"""create a new PackageModule"""
		Module.__init__(self, elm, level)
		self.name = elm.getAttribute("name")
		self.description = elm.getAttribute("description") or "no description"


	def getHTML(self):
		s =  '<div class="package level-%d" >\n'  % (self.level)
		s += '\t<h2 class="packagename">Package: %s</h2>\n' % (self.name)
		s += '\t<div class="packagedescription">%s</div>\n' % (self.description)
		s += '</div>'

		return s



class ClassModule(Module):

	__slots__ = ("name", "description")

	def __init__(self, elm, level=0):
		"""create a new ClassModule"""
		Module.__init__(self, elm, level)
		self.name = elm.getAttribute("name")
		self.description = elm.getAttribute("description") or "no description"


	def getHTML(self):
		s = '<div class="class level-%d">\n' % (self.level)
		s += '\t<h2 class="classname">%s</h2>\n' % (self.name)
		s += '\t<div class="classdescription">%s</div>\n' % (self.description)
		s += '</div>'
		return s



class GeneratorFactory:
	pass


class TOCGenerator:

	def __init__(self):
		pass


	@staticmethod
	def generateTOC(modules, target):
		
		# split into packages and classes.



		# prefix
		html = "<!DOCTYPE HTML>\n"
		html += "<html>\n"
		
		# head
		html += "<head>\n"
		html += "<title>Table Of Contents</title>\n"
		html += '<link rel="stylesheet" type="text/css" href="%s" />\n'  % Config.stylesheet
		html += "</head>\n"


		packageToc = ''
		classToc = ''
		functionToc = ''

		for m in modules:
			if isinstance(m, PackageModule):
				packageToc += m.getHTML()
			if isinstance(m, ClassModule):
				classToc += m.getHTML()


		html += '<h1>Packages</h1>\n'
		html += packageToc

		html += '<h1>Classes</h1>\n'
		html += classToc

		html += '<h1>Functions</h1>\n'
		


		html += "</html>\n"

		print html
		f = open(target, "w")

		f.write(html)







d = InFileReader("sample.xml")
parser = d.getParser()
modules = parser.getModules()
TOCGenerator.generateTOC(modules, "index.html")




