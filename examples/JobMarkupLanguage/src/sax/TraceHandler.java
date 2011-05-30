package sax;

               
import java.io.PrintWriter;
import java.io.StringWriter;
import java.util.Properties;

import org.xml.sax.Attributes;
import org.xml.sax.ContentHandler;
import org.xml.sax.ErrorHandler;
import org.xml.sax.Locator;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;
import org.xml.sax.SAXParseException;
import org.xml.sax.helpers.XMLReaderFactory;
import org.xml.sax.XMLReader;

import java.util.Stack;
import java.util.Enumeration;
import java.util.StringTokenizer;

public class TraceHandler implements ContentHandler, ErrorHandler {

    protected Stack xmlContextStack;
    protected Locator locator;

    public TraceHandler() {

    }

    private void writeHeading(String heading) {
      System.out.println();
      System.out.println("*** " + heading + " ***");
    }

    private void writeProperties(Properties p, boolean printLocateInfo) {
      StringWriter sw = new StringWriter();
      PrintWriter pw = new PrintWriter(sw);
      if (locator != null && printLocateInfo) {
        p.setProperty("locator.column", locator.getColumnNumber()+"");
        p.setProperty("locator.line", locator.getLineNumber()+"");
      }
      p.list(pw);
      StringTokenizer st = new StringTokenizer(sw.toString(), "\r\n");
      st.nextToken();
      String line = "";
      while (st.hasMoreTokens()) {
         String nextToken = st.nextToken();
         int padding = nextToken.length() % 25;
         for (int i=padding; i < 25; i++)
            nextToken = nextToken + " ";
         if (line.length() + nextToken.length() > 3*25) {
            System.out.println(line);
            line = "";
         }
         line = line + nextToken;
      }
      System.out.println(line);
    }


    public void characters(char[] ch, int start, int length) 
    {
       Properties p = new Properties();
       p.setProperty("start",start+"");
       p.setProperty("length",length+"");
       p.setProperty("ch",new String(ch, start, length));
       p.setProperty("ch.length", ch.length + "");
       
       StringBuffer text = new StringBuffer();
       for (int i=start; i < start+length; i++) {
          int pos=i-start;
          switch(ch[i]) {
            case '\t': text.append("\\t"); break;
            case '\r': text.append("\\r"); break;
            case '\n': text.append("\\n"); break;
            case ' ' : text.append("\\s"); break;
            default: text.append(ch[i]);
          }
       }
       p.setProperty("text", text.toString());

       writeHeading("characters");
       writeProperties(p, true);

    }

    public void endElement(String uri, String localName, String qName)
    {
       Properties p = new Properties();
       p.setProperty("uri", uri);
       p.setProperty("localName", localName);
       p.setProperty("qName", qName);
       writeHeading("endElement");
       writeProperties(p, true);
    } 

    public void endPrefixMapping(String prefix) 
    {
       Properties p = new Properties();
       p.setProperty("prefix", prefix);
       writeHeading("endPrefixMapping");
       writeProperties(p, true);
    }

    public void ignorableWhitespace(char ch[], int start, int length)
    {
       Properties p = new Properties();
       p.setProperty("start", start + "");
       p.setProperty("length", length + "");
       writeHeading("ignorableWhitespace");
       writeProperties(p, true);
    } 

    public void processingInstruction(String target, String data)
    {
       Properties p = new Properties();
       p.setProperty("target", target);
       p.setProperty("data", data);
       writeHeading("processingInstruction");
       writeProperties(p, true);
    }

    public void setDocumentLocator(Locator locator)
    {
       this.locator = locator;
       Properties p = new Properties();
       p.setProperty("locator.column", locator.getColumnNumber()+"");
       p.setProperty("locator.line", locator.getLineNumber()+"");
       p.setProperty("locator.pub.id", locator.getPublicId() + "");
       p.setProperty("locator.sys.id", locator.getSystemId() + "");
       writeHeading("processingInstruction");
       writeProperties(p, true);

    }

    public void skippedEntity(String name)
    {
       Properties p = new Properties();
       p.setProperty("name", name);
       writeHeading("skippedEntity");
       writeProperties(p, true);
    }

    public void startDocument() { 
       xmlContextStack = new Stack();

       writeHeading("startDocument");
    }

    public void endDocument() {
       writeHeading("endDocument");
    }


    public void startElement(String uri, String name, String qName,
                             Attributes attrs)
    {
       Properties p = new Properties();
       p.setProperty("name", name);
       p.setProperty("qName", qName);
       p.setProperty("uri", uri);
       writeHeading("startElement");
       writeProperties(p, true);
       if (attrs.getLength() > 0) {
          p = new Properties();
          for (int i=0; i < attrs.getLength(); i++) {
             p.setProperty( attrs.getQName(i), attrs.getValue(i) );
          }
          writeHeading("startElement: Attributes");
          writeProperties(p, false);
       }
    }


    public void startPrefixMapping(String prefix, String uri)
    {
       Properties p = new Properties();
       p.setProperty("prefix", prefix);
       p.setProperty("uri", uri);
       writeHeading("startPrefixMapping");
       writeProperties(p, true);
    }


    public void warning(SAXParseException ex) {
        System.err.println("[Warning] "+ ex);
    }

    public void error(SAXParseException ex) {
        System.err.println("[Error] "+ ex);

    }

    public void fatalError(SAXParseException ex) throws SAXException {
        System.err.println("[Fatal Error] " + ex);
        throw ex;
    }

}
