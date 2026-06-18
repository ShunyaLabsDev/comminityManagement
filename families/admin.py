from django.contrib import admin
from .models import Family, Member, ContactInfo


class MemberInline(admin.TabularInline):
    model = Member
    extra = 1
    fields = (
        'name', 'relation', 'gender', 'marital_status',
        'date_of_birth', 'blood_group',
        'mobile', 'whatsapp', 'email',
        'education', 'occupation', 'annual_income',
        'spouse_name', 'marriage_date',
        'any_disability',
    )
    show_change_link = True


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ('family_id', 'family_name', 'village', 'gotra', 'mobile', 'member_count', 'submitted_by', 'created_at')
    list_filter = ('village', 'gotra', 'business', 'is_active')
    search_fields = ('family_name', 'village', 'mobile')
    inlines = [MemberInline]
    list_per_page = 25
    readonly_fields = ('created_at',)

    def member_count(self, obj):
        return obj.member_count()
    member_count.short_description = 'Members'


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'family', 'relation', 'gender', 'marital_status', 'age', 'blood_group', 'mobile', 'education', 'occupation')
    list_filter = ('relation', 'gender', 'marital_status', 'blood_group', 'family__village', 'any_disability')
    search_fields = ('name', 'family__family_name', 'mobile', 'email', 'occupation')
    list_per_page = 25

    fieldsets = (
        ('Basic Info', {
            'fields': ('family', 'name', 'relation', 'gender', 'date_of_birth', 'marital_status', 'blood_group', 'photo')
        }),
        ('Contact', {
            'fields': ('mobile', 'whatsapp', 'email')
        }),
        ('Education & Occupation', {
            'fields': ('education', 'education_detail', 'occupation', 'occupation_detail', 'annual_income')
        }),
        ('Marriage', {
            'fields': ('spouse_name', 'marriage_date'),
            'classes': ('collapse',),
        }),
        ('Health', {
            'fields': ('any_disability', 'disability_detail'),
            'classes': ('collapse',),
        }),
    )


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    pass
