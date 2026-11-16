import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

public class UserDirectory {
    private final Map<String, User> users = new HashMap<>();

    /** email may be null or blank when we don't know it */
    public void add(String id, String name, String email) {
        users.put(id, new User(id, name, email));
    }

    private Optional<User> find(String id) {
        return Optional.ofNullable(users.get(id));
    }

    public String contactLine(String id) {
        return find(id)
                .map(user -> user.email()
                        .map(email -> user.name() + " <" + email + ">")
                        .orElse(user.name() + " (no email)"))
                .orElse("unknown user");
    }

    public String domainOf(String id) {
        return find(id)
                .flatMap(User::email)
                .filter(email -> email.contains("@"))
                .map(email -> email.substring(email.indexOf('@') + 1).toLowerCase())
                .orElse("n/a");
    }

    public int countWithEmail() {
        return (int) users.values().stream().filter(user -> user.email().isPresent()).count();
    }
}
