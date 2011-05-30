package job;
               
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;

import org.xml.sax.Attributes;
import org.xml.sax.ContentHandler;
import org.xml.sax.Parser;
import org.xml.sax.SAXException;
import org.xml.sax.SAXParseException;
import org.xml.sax.helpers.XMLReaderFactory;

import java.util.Vector;
import java.util.Stack;
import java.util.Enumeration;

public class JMLParser extends HandlerBase {

    private static final String 
        DEFAULT_PARSER_NAME = "org.apache.xerces.parsers.SAXParser";

    protected boolean canonical;

    /* pushdown of context information */
    protected Stack cnJobStack;

    /* the current job construct always sits atop the stack. This
     * is primarily for coding convenience.
     */
    protected Job currentJob;

    protected Job successfullyParsedJob = null;

    public JMLParser(boolean canonical) throws UnsupportedEncodingException {
        this(null, canonical);
    }

    protected JMLParser(String encoding, boolean canonical)
	throws UnsupportedEncodingException {

        if (encoding == null) {
            encoding = "UTF8";
        }
        this.canonical = canonical;
    }

    public static void parse(String parserName, String uri, boolean canonical) {
        try {
            
            JMLParser handler = new JMLParser(canonical);
            XMLReader xmlReader = XMLReaderFactory.createXMLReader();
            xmlReader.setContentHandler(handler);
            xmlReader.setErrorHandler(handler);
            xmlReader.parse(new InputSource(uri));

            Job ticket = handler.getJobTicket();
            System.out.println("Parse Successful!");
            System.out.println(ticket);
        }
        catch (Exception e) {
            System.out.println("Exception " + e);
            e.printStackTrace(System.err);
        }

    }

    public Job getJobTicket() {
       return currentJob;
    }

    /*
     * SAX2 ContentHandler Methods
     */

    public void processingInstruction(String target, String data) {
       /* not used in the JML System */
    }

    public void startDocument() { 
        cnJobStack = new Stack();
        currentJob = new CompositeJob(CompositeJob.T_SEQ);
        cnJobStack.push(currentJob);
    }


    public void startElement(String uri, String name, String qName,
                             Attributes attrs)
    {

	if (name.equalsIgnoreCase("ticket"))
	    startTicket(name, attrs);
	else if (name.equalsIgnoreCase("job"))
	    startJob(name, attrs);
	else if (name.equalsIgnoreCase("par"))
	    startCompositeJob(name, attrs);
	else if (name.equalsIgnoreCase("seq"))
	    startCompositeJob(name, attrs);
        else if (name.equalsIgnoreCase("property"))
            startProperty(name, attrs);
	else 
	    startConsume(name, attrs);
    }

    public void startTicket(String name, Attributes attrs) {
       // This is teh beginning of the job ticket. I haven't decided
       // yet whether multiple job tickets are permitted in a single
       // file but will talk to John about this. We might as well
       // leave room for growth!
    }


    public void startJob(String name, Attributes attrs) {

    /* note: a validating parser will guarantee that name, type, nodes
     * and code all appear at least once in the element. This is why
     * I'm not putting any checks here.
     */
        String jname = attrs.getValue("name");
        String type = attrs.getValue("type");
        String nodes = attrs.getValue("nodes");
        String code = attrs.getValue("code");
        String mainclass = attrs.getValue("mainclass");
        String mainmethod = attrs.getValue("mainmethod");
        UserJob j = new UserJob(jname,type,nodes,code,mainclass,mainmethod);
        currentJob.addJob(j);
        currentJob = j;
        cnJobStack.push(currentJob);
    }

    public void startCompositeJob(String name, Attributes attrs) {
        CompositeJob cj;
        if (name.equalsIgnoreCase("seq")) 
          cj = new CompositeJob(CompositeJob.T_SEQ);
        else
          cj = new CompositeJob(CompositeJob.T_PAR);
        currentJob.addJob(cj);
        currentJob = cj;
        cnJobStack.push(cj);        
    }

    public void startProperty(String name, Attributes attrs) {
        String pname = attrs.getValue("name");
        String value = attrs.getValue("value");
        currentJob.setProperty(pname, value);
    }

    public void startConsume(String name, Attributes attrs) {
        System.out.println("Warning: Unexpected element " + name);
        System.out.println("Warning: this message should not happen in a validating parser.");
    }

    public void characters(char ch[], int start, int length) {
    }

    public void ignorableWhitespace(char ch[], int start, int length) {
    } 

    public void endElement(String uri, String name, String qName) {
	if (name.equalsIgnoreCase("ticket"))
           endTicket();
	else if (name.equalsIgnoreCase("job"))
	    endJob();
	else if (name.equalsIgnoreCase("par"))
	    endJob();
	else if (name.equalsIgnoreCase("seq"))
	    endJob();
        else if (name.equalsIgnoreCase("property"))
            endNop();

    }

    public void endTicket() {
       Enumeration jobStackEnum = cnJobStack.elements();
       while (jobStackEnum.hasMoreElements()) {
         Object element = jobStackEnum.nextElement();
         if (element instanceof Job) {
            Job job = (Job) element;
            /* GKT: Could do something here if desired! */
         }
       }
    }

    public void endJob() {
       cnJobStack.pop();
       currentJob = (Job) cnJobStack.peek();
    }
       

    public void endNop() {}


    public void endDocument() {
        successfullyParsedJob = currentJob;
    }

    public void warning(SAXParseException ex) {
        System.err.println("[Warning] "+
                           getLocationString(ex)+": "+
                           ex.getMessage());
    }

    public void error(SAXParseException ex) {
        System.err.println("[Error] "+
                           getLocationString(ex)+": "+
                           ex.getMessage());
    }

    public void fatalError(SAXParseException ex) throws SAXException {
        System.err.println("[Fatal Error] "+
                           getLocationString(ex)+": "+
                           ex.getMessage());
        throw ex;
    }

    private String getLocationString(SAXParseException ex) {
        StringBuffer str = new StringBuffer();

        String systemId = ex.getSystemId();
        if (systemId != null) {
            int index = systemId.lastIndexOf('/');
            if (index != -1) 
                systemId = systemId.substring(index + 1);
            str.append(systemId);
        }
        str.append(':');
        str.append(ex.getLineNumber());
        str.append(':');
        str.append(ex.getColumnNumber());

        return str.toString();

    }
    protected String normalize(String s) {
        StringBuffer str = new StringBuffer();

        int len = (s != null) ? s.length() : 0;
        for (int i = 0; i < len; i++) {
            char ch = s.charAt(i);
            switch (ch) {
                case '<': {
                    str.append("&lt;");
                    break;
                }
                case '>': {
                    str.append("&gt;");
                    break;
                }
                case '&': {
                    str.append("&amp;");
                    break;
                }
                case '"': {
                    str.append("&quot;");
                    break;
                }
                case '\r':
                case '\n': {
                    if (canonical) {
                        str.append("&#");
                        str.append(Integer.toString(ch));
                        str.append(';');
                        break;
                    }
                    // else, default append char
                }
                default: {
                    str.append(ch);
                }
            }
        }

        return str.toString();

    }


    public static void main(String argv[]) {

        if (argv.length == 0) {
            printUsage();
            System.exit(1);
        }

        String  parserName = DEFAULT_PARSER_NAME;
        boolean canonical  = false;

        // Replace all of this with John's CommandLineParser class.
        for (int i = 0; i < argv.length; i++) {
            String arg = argv[i];

            // options
            if (arg.startsWith("-")) {
                if (arg.equals("-p")) {
                    if (i == argv.length - 1) {
                        System.err.println("error: missing parser name");
                        System.exit(1);
                    }
                    parserName = argv[++i];
                    continue;
                }

                if (arg.equals("-c")) {
                    canonical = true;
                    continue;
                }

                if (arg.equals("-h")) {
                    printUsage();
                    System.exit(1);
                }
            }

            System.err.println(arg+':');
            parse(parserName, arg, canonical);
            System.out.println();
        }

    } 

    private static void printUsage() {

        System.err.println("usage: java sax.JMLParser (options) uri ...");
        System.err.println();
        System.err.println("options:");
        System.err.println("  -p name  Specify SAX parser by name.");
        System.err.println("           Default parser: "+DEFAULT_PARSER_NAME);
        System.err.println("  -c       Canonical XML output.");
        System.err.println("  -h       This help screen.");

    }

}
