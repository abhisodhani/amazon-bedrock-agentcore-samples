-- Check if view exists
SHOW VIEWS IN connect-datalake-local;

-- Alternative check
SELECT * FROM information_schema.views 
WHERE table_name = 'contact_record_qs_cr_dataset';

-- Test the view
SELECT COUNT(*) FROM contact_record_qs_cr_dataset LIMIT 1;