import java.util.HashMap;
import java.util.Map;

public class UserDirectory {
    private final Map<String, User> users = new HashMap<>();

    /** email may be null or blank when we don't know it */
    public void add(String id, String name, String email) {
        users.put(id, new User(id, name, email));
    }

    private User find(String id) {
        return users.get(id);
    }

    private String emailOf(String id) {
        User user = find(id);
        if (user == null) {
            return null;
        }
        if (user.email == null || user.email.isBlank()) {
            return null;
        }
        return user.email;
    }

    public String contactLine(String id) {
        User user = find(id);
        if (user == null) {
            return "unknown user";
        }
        String email = emailOf(id);
        if (email == null) {
            return user.name + " (no email)";
        }
        return user.name + " <" + email + ">";
    }

    public String domainOf(String id) {
        String email = emailOf(id);
        if (email == null) {
            return "n/a";
        }
        int at = email.indexOf('@');
        if (at < 0) {
            return "n/a";
        }
        return email.substring(at + 1).toLowerCase();
    }

    public int countWithEmail() {
        int count = 0;
        for (String id : users.keySet()) {
            if (emailOf(id) != null) {
                count++;
            }
        }
        return count;
    }
}
