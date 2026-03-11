-- XGrivanceMon Database Schema
-- TursoDB (SQLite over HTTP)

CREATE TABLE IF NOT EXISTS authorities (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    handle TEXT UNIQUE NOT NULL,
    city TEXT,
    state TEXT,
    type TEXT CHECK(type IN ('metro', 'bus', 'rail', 'mixed', 'corporation')),
    schedule_day INTEGER, -- 0=Monday, 6=Sunday
    schedule_hour INTEGER,
    schedule_minute INTEGER DEFAULT 0,
    active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS complaints (
    id TEXT PRIMARY KEY,
    x_post_id TEXT UNIQUE NOT NULL,
    authority_id TEXT REFERENCES authorities(id),
    content TEXT NOT NULL,
    author_handle TEXT,
    posted_at DATETIME NOT NULL,
    url TEXT,
    category TEXT CHECK(category IN ('frequency', 'infrastructure', 'staff', 'route', 'fare', 'other')),
    sentiment REAL CHECK(sentiment BETWEEN -1 AND 1),
    has_response BOOLEAN DEFAULT 0,
    response_time_hours REAL,
    response_url TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reports (
    id TEXT PRIMARY KEY,
    authority_id TEXT REFERENCES authorities(id),
    week_start DATE NOT NULL,
    week_end DATE NOT NULL,
    report_markdown TEXT,
    total_complaints INTEGER,
    total_responses INTEGER,
    avg_response_time REAL,
    resolution_rate REAL,
    top_categories TEXT, -- JSON array
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_complaints_authority ON complaints(authority_id);
CREATE INDEX IF NOT EXISTS idx_complaints_posted_at ON complaints(posted_at);
CREATE INDEX IF NOT EXISTS idx_reports_authority ON reports(authority_id);

-- Insert default authorities (12 transport monitoring agents)
INSERT INTO authorities (id, name, handle, city, state, type, schedule_day, schedule_hour) VALUES
('mtc-chennai', 'MTC Chennai', 'MtcChennai', 'Chennai', 'Tamil Nadu', 'bus', 2, 9),
('best-mumbai', 'BEST Mumbai', 'myBESTBus', 'Mumbai', 'Maharashtra', 'bus', 0, 9),
('dtc-delhi', 'DTC Delhi', 'dtc_india', 'Delhi', 'Delhi', 'bus', 4, 9),
('bmtc-bangalore', 'BMTC Bangalore', 'BMTC_BENGALURU', 'Bangalore', 'Karnataka', 'bus', 1, 9),
('ksrtc-kerala', 'KSRTC Kerala', 'KSRTC_Kerala', 'Kerala', 'Kerala', 'bus', 2, 9),
('upsrtc-up', 'UPSRTC UP', 'UPSRTCHQ', 'Uttar Pradesh', 'Uttar Pradesh', 'bus', 5, 9),
('tgsrtc-telangana', 'TGSRTC Telangana', 'TGSRTCHQ', 'Telangana', 'Telangana', 'bus', 6, 9),
('chennai-one', 'Chennai ONE', 'Chennai_One', 'Chennai', 'Tamil Nadu', 'mixed', 0, 14),
('drm-chennai', 'Chennai DRM', 'drmchennai', 'Chennai', 'Tamil Nadu', 'rail', 2, 16),
('cumta-chennai', 'Chennai CUMTA', 'cumtaOfficial', 'Chennai', 'Tamil Nadu', 'mixed', 3, 17),
('cmrl-chennai', 'Chennai Metro', 'cmrlchennai', 'Chennai', 'Tamil Nadu', 'metro', 1, 15),
('chennai-corp', 'Chennai Corporation', 'chennaicorp', 'Chennai', 'Tamil Nadu', 'corporation', 0, 11);
