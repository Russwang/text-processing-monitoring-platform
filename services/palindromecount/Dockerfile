FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /app
COPY pom.xml ./
COPY src ./src
RUN mvn --batch-mode verify
FROM eclipse-temurin:17-jre
WORKDIR /app
COPY --from=build /app/target/classes ./classes
EXPOSE 9000
CMD ["java", "-cp", "classes", "PalindromeCount"]
