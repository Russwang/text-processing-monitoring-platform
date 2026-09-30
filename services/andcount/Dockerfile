FROM ruby:3.3

RUN gem install bundler -v 2.5.23

WORKDIR /usr/src/app

COPY Gemfile Gemfile.lock ./

RUN bundle _2.5.23_ install

COPY . .

EXPOSE 4567

CMD ["bundle", "exec", "rackup", "-o", "0.0.0.0", "-p", "4567", "config.ru"]
