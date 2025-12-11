from supabase import create_client
from config2 import SUPABASE_URL, SUPABASE_KEY



supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
