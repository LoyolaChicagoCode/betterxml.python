package job;

import java.io.*;
import java.util.*;

public class UserJob extends Job {

  public static final int T_SERIAL = 100;
  public static final int T_PARALLEL = 101;
  public static final int T_COORDINATED = 102;
  public static final int T_PERSISTENT = 103;

  private String name;
  private int type;
  private int numberOfProcessors;
  private String codeLocation;
  private String mainMethod;
  private String mainClass; 

  public UserJob(String name, String codeLocation, String mainClass, String mainMethod) {
     this(name, UserJob.T_SERIAL, 1, codeLocation, mainClass, mainMethod);
  }

  public UserJob(String name, int type, int numberOfProcessors,
                 String codeLocation, String mainClass, String mainMethod) {
     super();
     this.name = name;
     this.type = type;
     this.numberOfProcessors = numberOfProcessors;
     this.codeLocation = codeLocation;
     this.mainClass = mainClass;
     this.mainMethod = mainMethod;
  }


  public UserJob(String name, String type, String numberOfProcessors,
                 String codeLocation, String mainClass, String mainMethod) {
     super();
     this.name = name;
     if (type.equalsIgnoreCase("serial"))
        this.type = T_SERIAL;
     else if (type.equalsIgnoreCase("parallel"))
        this.type = T_SERIAL;
     else if (type.equalsIgnoreCase("coordinated"))
        this.type = T_SERIAL;
     else if (type.equalsIgnoreCase("persistent"))
        this.type = T_PERSISTENT;
     else
        this.type = T_SERIAL;
     try {
       this.numberOfProcessors = Integer.parseInt(numberOfProcessors);
     } catch(Exception e) {
       this.numberOfProcessors = 1;
     }
     this.codeLocation = codeLocation;
     this.mainMethod = mainMethod;
     this.mainClass = mainClass;
  }


  public String toString() {
    return toString(0);
  }

  public String toString(int level) {
    String encoding = "\n" + tabs(level) + "user job ";
    switch(type) {
      case T_SERIAL: encoding += "sequential"; break;
      case T_PARALLEL: encoding += "parallel"; break;
      case T_COORDINATED: encoding += "coordinated"; break;
      case T_PERSISTENT: encoding += "persistent"; break;
    }
    if (type != T_SERIAL)
      encoding += " " + numberOfProcessors + " processors";
    encoding += " " + codeLocation;

    encoding += " entry point " + mainClass + "." + mainMethod + "\n";
    Enumeration props = properties.keys();
    while (props.hasMoreElements()) {
      encoding += tabs(level);
      Object key = props.nextElement();
      encoding += key + "=" + properties.get(key) + "\n";
    }
    return encoding;
  }
}
