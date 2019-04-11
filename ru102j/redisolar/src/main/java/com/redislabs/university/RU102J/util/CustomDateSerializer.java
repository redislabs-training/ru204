package com.redislabs.university.RU102J.util;

import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.JavaType;
import com.fasterxml.jackson.databind.SerializerProvider;
import com.fasterxml.jackson.databind.deser.std.StdDeserializer;
import com.fasterxml.jackson.databind.ser.std.StdSerializer;

import java.io.IOException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Date;

public class CustomDateSerializer extends StdSerializer<ZonedDateTime> {

    DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd hh:mm:ss z");

    protected CustomDateSerializer(Class<ZonedDateTime> t) {
        super(t);
    }

    protected CustomDateSerializer(JavaType type) {
        super(type);
    }

    protected CustomDateSerializer(Class<?> t, boolean dummy) {
        super(t, dummy);
    }

    protected CustomDateSerializer(StdSerializer<?> src) {
        super(src);
    }


    @Override
    public void serialize(ZonedDateTime zonedDateTime, JsonGenerator jsonGenerator,
                          SerializerProvider serializerProvider) throws IOException {
        jsonGenerator.writeString(formatter.format(zonedDateTime));

    }
}
