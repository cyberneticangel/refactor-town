public class User {
    public final String id;
    public final String name;
    public final String email; // may be null!

    public User(String id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }
}
