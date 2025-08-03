package models;

import utils.Constants;
import utils.Contact;
import utils.Errors;

import java.lang.reflect.Field;
import java.lang.reflect.Modifier;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.stream.Stream;

abstract class ContactImpl implements Contact {
    protected String phone;
    protected String name;
    private boolean isPerson;
    private final LocalDateTime created;
    private LocalDateTime edited;

    ContactImpl() {
        created = LocalDateTime.now();
        edited = LocalDateTime.now();
    }

    private List<Field> getVisibleFields() {
        List<Field> fields = new ArrayList<>(
            Stream.of(this.getClass().getSuperclass().getDeclaredFields())
                .filter(x -> !Modifier.isPrivate(x.getModifiers()) && !Modifier.isStatic(x.getModifiers()))
                .toList());
        fields.addAll(List.of(this.getClass().getDeclaredFields()));
        return fields;
    }

    @Override
    public String getName() {
        return name != null ? name : Constants.EMPTY_FIELD_VALUE;
    }

    @Override
    public String getContactFields() {
        return getVisibleFields().stream()
            .map(Field::getName)
            .reduce("", (s, f) -> String.join(", ", s, f)).substring(2);
    }

    public String getSearchableData() {
        return getVisibleFields().stream().map(f -> {
            try {
                f.setAccessible(true);
                return f.get(this);
            } catch (IllegalAccessException e) {
                throw new RuntimeException(e);
            }
        }).filter(Objects::nonNull)
            .map(Object::toString)
            .reduce("", (s, v) -> s + v);
    }

    protected void setPersonFlag(boolean flag) {
        isPerson = flag;
    }

    protected String getPhoneNumber() {
        return phone != null ? phone : Constants.EMPTY_FIELD_VALUE;
    }

    protected void setName(String input) {
        if (!input.equals("Machete")) {
            this.name = input;
        }
        else {
            throw new IllegalArgumentException("You don't contact Machete");
        }
    }

    protected void setPhoneNumber(String input) throws IllegalArgumentException {
        if (input.matches(Constants.PHONE_PATTERN)) {
            this.phone = input;
        }
        else {
            this.phone = null;
            System.out.println(Errors.WRONG_NUMBER);
        }
    }

    protected void onEdit() {
        edited = LocalDateTime.now();
    }

    protected String getTimestamps() {
        return "Time created: %s\nTime last edit: %s".formatted(created, edited);
    }

    abstract protected String getContactCard();
    abstract protected void editField(String fieldName, Object newValue) throws IllegalArgumentException;
}
