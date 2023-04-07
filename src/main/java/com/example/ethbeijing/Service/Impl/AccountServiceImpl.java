package com.example.ethbeijing.Service.Impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.ethbeijing.Service.AccountServicce;
import com.example.ethbeijing.entity.Account;
import com.example.ethbeijing.mapper.AccountMapper;
import org.springframework.stereotype.Service;

@Service
public class AccountServiceImpl extends ServiceImpl<AccountMapper, Account> implements AccountServicce{
}
