import java.util.*;

public class Politician
{
    // Class variables
    private String politicianID;
    private String fullName;
    private HashMap trades;

    // Constructor
    public Politician(String name, String Id)
    { politicianID = Id; fullName = name; }

    // Getters
    public String getPoliticianID() 
    { return politicianID; }

    public String getFullName()
    { return fullName; }

    public HashMap getTrades()
    { return trades; }


    // Setter
    public void setPoliticianID(String polID)
    { politicianID = polID; }

    public void setFullName(String name)
    { fullName = name; }

    public void setTrades(HashMap t)
    { trades = t; }
}