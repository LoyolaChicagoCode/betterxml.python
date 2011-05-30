import java.util.Properties;
import java.io.*;

public class PropertiesHack {

   public static void main(String args[]) {
     Properties p = new Properties();
     p.setProperty("x", 1 + "");
     p.setProperty("y", "test");
     PrintWriter pw = new PrintWriter(System.out, true);
     p.list(pw);
   }
}
