INSERT INTO plots (lab_id, plot)
SELECT labs.id, plotnums.plot
FROM labs, (SELECT generate_series(1, 20) AS plot) AS plotnums
ON CONFLICT DO NOTHING;

UPDATE plots SET current_seed_sample =
(CASE
    WHEN plot % 4 = 1 THEN 'AXM477'
    WHEN plot % 4 = 2 THEN 'AXM478'
    WHEN plot % 4 = 3 THEN 'AXM479'
    WHEN plot % 4 = 0 THEN 'AXM480'
    ELSE ''
END)
WHERE plot > 0;
