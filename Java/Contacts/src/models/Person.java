package models;

import utils.Constants;
import utils.Errors;

import java.io.*;
import java.time.LocalDate;

class Person extends ContactImpl implements Serializable {
    @Serial
    private static final long serialVersionUID = 1L;
    private String surname;
    private Character gender;
    private LocalDate birthDate;

    Person() {
        setPersonFlag(true);
    }

    private String getSurname() {
        return surname != null ? surname : Constants.EMPTY_FIELD_VALUE;
    }

    private String getGender() {
        return gender != null ? String.valueOf(gender) : Constants.EMPTY_FIELD_VALUE;
    }

    private LocalDate getBirthDate() {
        return birthDate;
    }

    void setSurname(String input) {
        this.surname = input;
    }

    void setGender(Character g) {
        if (g.equals('M') || g.equals('F')) {
            this.gender = g;
        }
        else {
            System.out.println("Bad gender!");
        }
    }

    void setBirthDate(LocalDate date) {
        if (date != null) {
            this.birthDate = date;
        }
        else {
            System.out.println("Bad date!");
        }
    }

    @Override
    public String toString() {
        return "%s %s".formatted(getName(), getSurname());
    }

    @Override
    protected void editField(String fieldName, Object newValue) throws IllegalArgumentException {
        switch (fieldName) {
            case "name" -> setName((String)newValue);
            case "surname" -> setSurname((String)newValue);
            case "number" -> setPhoneNumber((String)newValue);
            case "gender" -> setGender(((String)newValue).charAt(0));
            case "birth" -> setBirthDate((LocalDate)newValue);
            default -> throw new IllegalArgumentException(Errors.NO_SUCH_FIELD.formatted(fieldName));
        }
        onEdit();
    }

    @Override
    protected String getContactCard() {
        return new StringBuilder()
            .append("Name: %s\n".formatted(getName()))
            .append("Surname: %s\n".formatted(getSurname()))
            .append("Birth date: %s\n".formatted(getBirthDate() != null ? getBirthDate() : Constants.EMPTY_FIELD_VALUE))
            .append("Gender: %s\n".formatted(getGender()))
            .append("Number: %s\n".formatted(getPhoneNumber()))
            .append(getTimestamps())
            .toString();
    }
}