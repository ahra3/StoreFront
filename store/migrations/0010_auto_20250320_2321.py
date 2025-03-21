# store/migrations/0010_custom_change_id_to_uuid.py
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('store', '0009_alter_orderitem_product_alter_product_collection_and_more'),  # Adjust based on your previous migration name
    ]

    operations = [
        # Step 1: Drop the foreign key constraint on cart_id in store_cartitem (if it exists)
        migrations.RunSQL(
            'ALTER TABLE store_cartitem DROP CONSTRAINT store_cartitem_cart_id_4f60ac05_fk_store_cart_id;',  # Use the actual constraint name
            reverse_sql='ALTER TABLE store_cartitem ADD CONSTRAINT store_cartitem_cart_id_4f60ac05_fk_store_cart_id FOREIGN KEY (cart_id) REFERENCES store_cart(id);'
        ),
        # Step 2: Drop the old id column in store_cart
        migrations.RunSQL(
            'ALTER TABLE store_cart DROP COLUMN id;',
            reverse_sql='ALTER TABLE store_cart ADD COLUMN id bigint NOT NULL;'
        ),
        # Step 3: Add a new id column of type UUID in store_cart
        migrations.RunSQL(
            'ALTER TABLE store_cart ADD COLUMN id uuid NOT NULL DEFAULT gen_random_uuid();',
            reverse_sql='ALTER TABLE store_cart DROP COLUMN id;'
        ),
        # Step 4: Recreate the primary key constraint on the new id column
        migrations.RunSQL(
            'ALTER TABLE store_cart ADD PRIMARY KEY (id);',
            reverse_sql='ALTER TABLE store_cart DROP CONSTRAINT store_cart_pkey;'
        ),
        # Step 5: Drop the old cart_id column in store_cartitem
        migrations.RunSQL(
            'ALTER TABLE store_cartitem DROP COLUMN cart_id;',
            reverse_sql='ALTER TABLE store_cartitem ADD COLUMN cart_id bigint NOT NULL;'
        ),
        # Step 6: Add a new cart_id column of type UUID in store_cartitem
        migrations.RunSQL(
            'ALTER TABLE store_cartitem ADD COLUMN cart_id uuid;',
            reverse_sql='ALTER TABLE store_cartitem DROP COLUMN cart_id;'
        ),
        # Step 7: Recreate the foreign key constraint with the desired name
        migrations.RunSQL(
            'ALTER TABLE store_cartitem ADD CONSTRAINT store_cartitem_cart_id_fkey FOREIGN KEY (cart_id) REFERENCES store_cart(id);',
            reverse_sql='ALTER TABLE store_cartitem DROP CONSTRAINT store_cartitem_cart_id_fkey;'
        ),
    ]