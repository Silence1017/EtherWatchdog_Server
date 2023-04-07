package com.example.ethbeijing.entity;

import com.baomidou.mybatisplus.annotation.FieldFill;
import com.baomidou.mybatisplus.annotation.TableField;
import lombok.Data;

import java.io.Serializable;
import java.time.LocalDateTime;

@Data
public class Account implements Serializable {
    private static final long serialVersionUID=1L;
    private String username;
    private String password;
    @TableField(fill= FieldFill.INSERT)
    private LocalDateTime createTime;
}
