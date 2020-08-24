#!/usr/bin/env python
# coding=utf-8

from rest_framework.permissions import BasePermission

class Permission(BasePermission):
    def has_permission(self, request, view):
        return  True
