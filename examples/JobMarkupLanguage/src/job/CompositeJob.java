package job;

import java.io.*;
import java.util.*;

public class CompositeJob extends Job {
  public static final int T_SEQ = 200;
  public static final int T_PAR = 201;

  private int type;

  public CompositeJob(int type) {
    super();
    this.type = type;
  }

  public String toString() {
    return toString(0);
  }

  public String toString(int level) {
    String encoding = "\n";
    encoding += tabs(level);
    if (type == CompositeJob.T_PAR)
      encoding += "parallel:";
    else
      encoding += "sequential:";
    encoding += "\n";
    encoding += super.toString(level+1);
    return encoding;
  }
}
