
CREATE TABLE users (
    id UUID PRIMARY KEY,
    name VARCHAR,
    age_group TEXT,
    nationality TEXT,
    region TEXT
);


CREATE TABLE guides (
    id UUID PRIMARY KEY,
    name TEXT,
    bio TEXT,
    region TEXT,
    rating NUMERIC
);


CREATE TABLE guide_tags (
    id UUID PRIMARY KEY,
    guide_id UUID REFERENCES guides(id) ON DELETE CASCADE,
    tag TEXT
);


CREATE TABLE user_interests (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    interest TEXT
);


CREATE TABLE interactions (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    guide_id UUID REFERENCES guides(id) ON DELETE CASCADE,
    interest_match_score FLOAT8,
    created_at TIMESTAMPTZ DEFAULT now()
);
