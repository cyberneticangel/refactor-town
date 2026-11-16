import java.util.Optional;

/** email may be null or blank in the constructor; email() never returns null. */
public record User(String id, String name, Optional<String> email) {
    public User(String id, String name, String email) {
        this(id, name, Optional.ofNullable(email).filter(e -> !e.isBlank()));
    }
}
