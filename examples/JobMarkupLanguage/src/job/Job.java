package job;

import java.io.*;
import java.util.*;

public abstract class Job {

    protected Vector subJobs = new Vector();
    protected Hashtable properties = new Hashtable(); 

    public Job() {}

    public void addJob(Job job) {
	subJobs.addElement(job);
    }
    
    Enumeration getJobEnumeration() {
	return subJobs.elements();
    }

    public String toString(int level) {
	String encoding = "\n";
	Enumeration sj = subJobs.elements();
	while (sj.hasMoreElements()) {
	    Job j = (Job)sj.nextElement();
	    encoding += tabs(level) + j.toString(level) + "\n";
	}
	return encoding;
    }

    public String toString() {
	return toString(0);
    }

    public String tabs(int level) {
	String tab = "";
	for (int i=0; i < level; i++) tab += "  ";
	return tab;
    }

    public void setProperty(String key, String value) {
        properties.put(key,value);
    }

    public String getProperty(String key) {
        return (String) properties.get(key);
    }


    public static void main(String args[]) {

	/* Let's build a job graph. */

	UserJob j1 = new UserJob("j1",UserJob.T_SERIAL,1,"http://www/cn/j1.jar","mainclass","mainmethod");
	UserJob j2 = new UserJob("j2",UserJob.T_PARALLEL,2,"http://www/cn/j2.jar","mainclass","mainmethod");
	UserJob j3 = new UserJob("j3",UserJob.T_COORDINATED,4,"http://www/cn/j3.jar","mainclass","mainmethod");
	UserJob j4 = new UserJob("j3",UserJob.T_PARALLEL,2,"http://www/cn/j4.jar","mainclass","mainmethod");
	UserJob j5 = new UserJob("j3",UserJob.T_PARALLEL,2,"http://www/cn/j5.jar","mainclass","mainmethod");
	UserJob j6 = new UserJob("j3",UserJob.T_PARALLEL,2,"http://www/cn/j6.jar","mainclass","mainmethod");
	UserJob j7 = new UserJob("j3",UserJob.T_PARALLEL,2,"http://www/cn/j7.jar","mainclass","mainmethod");

	j1.setProperty("j1","j1 in prop");
	j1.setProperty("j1b","j1b in prop");
	j2.setProperty("j2","j2 in prop");
	j2.setProperty("j2b","j2b in prop");
	j3.setProperty("j3","j2 in prop");
	j4.setProperty("j4","j3 in prop");
	j5.setProperty("j5","j4 in prop");
	j6.setProperty("j6","j5 in prop");
	j7.setProperty("j7","j6 in prop");

	Job par1 = new CompositeJob(CompositeJob.T_PAR);
	Job par2 = new CompositeJob(CompositeJob.T_PAR);
	Job seq1 = new CompositeJob(CompositeJob.T_SEQ);

	par1.addJob(j2);
	par1.addJob(j3);
	par2.addJob(j5);
	par2.addJob(j6);
	seq1.addJob(j1);
	seq1.addJob(par1);
	seq1.addJob(j4);
	seq1.addJob(par2);
	seq1.addJob(j7);
	System.out.println(seq1);
    }
}
