package models;

import utils.Constants;
import utils.Errors;

import java.io.Serial;
import java.io.Serializable;

class Organization extends ContactImpl implements Serializable {
    @Serial
    private static final long serialVersionUID = 1L;
    private String address;

    Organization() {
        setPersonFlag(false);
    }

    String getAddress() {
        return address != null ? address : Constants.EMPTY_FIELD_VALUE;
    }

    void setAddress(String input) {
        if (input != null && !input.isBlank()) {
            this.address = input;
        }
        else {
            throw new IllegalArgumentException("Bad address!");
        }
    }

    @Override
    protected void editField(String fieldName, Object newValue) throws IllegalArgumentException {
        switch (fieldName) {
            case "name" -> setName((String)newValue);
            case "number" -> setPhoneNumber((String)newValue);
            case "address" -> setAddress((String)newValue);
            default -> throw new IllegalArgumentException(Errors.NO_SUCH_FIELD.formatted(fieldName));
        }
        onEdit();
    }

    @Override
    public String toString() {
        return getName();
    }

    @Override
    protected String getContactCard() {
        return new StringBuilder()
            .append("Organization name: %s\n".formatted(getName()))
            .append("Address: %s\n".formatted(getAddress()))
            .append("Number: %s\n".formatted(getPhoneNumber()))
            .append(getTimestamps())
            .toString();
    }
}

